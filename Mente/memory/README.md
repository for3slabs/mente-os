# memory/ — what the system must not forget

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and its README travel; ⛔ **the content never does.**
Exception: `principles/`, which is engine doctrine and ships whole.
**Governance:** `owner` in `piezas.tsv`

---

## What this folder is

Everything that must survive a context reset. When a session ends — deliberately or because the
context filled up — the conversation is gone: the code is still on disk, but **the reasoning
behind it is not**. This folder is where the reasoning was written down before that happened.

> ⭐ **The exact counterpart of `cache/`.** Losing `cache/` costs one slower run. **Losing
> `memory/` loses knowledge** — and nothing announces the loss, because the work still looks
> finished from the outside.

---

## ⭐ THE PROBLEM THIS FOLDER EXISTS TO SOLVE

Without it, an AI resuming work has one option: read the whole project and **infer** what was
happening.

| | Reconstructing by inference | Reading what was written |
|---|---|---|
| Cost | expensive — the entire tree | one small file |
| Accuracy | a guess | what actually happened |
| ⭐ The real danger | **it guesses wrong and sounds exactly as confident** | — |

⛔ **A reset is a cut, not a save.** Whatever is not on disk is gone with no warning. That is the
origin of the worst failure mode in this system: *it said everything was fine before the reset,
and after the reset it said things were still broken.* Both statements came from the same tree —
only the memory differed.

---

## The three kinds of memory here

They are not interchangeable, and mixing them is what makes this folder unusable.

### 1 · The cold-start brief — where we left off

⭐ **The single file guaranteed to be read when work resumes.** It answers: where we stopped, what
the next step is, what is blocking, and where to look for more.

⛔ **It has a hard size ceiling, enforced by a script — not by good intentions.** Its whole value
is that it is small enough to always be read. A brief that grows into a history stops being read
in full, and a brief read in half is worse than none: it looks complete.

> ⭐ **You do not write it by hand at the end of a marathon.** The session-closing routine asks
> what happened and writes it, and the pre-reset check **refuses** while it is out of date.

**When it grows past its ceiling, the history moves to the logbook — the brief keeps the state.**

### 2 · Open items — what is not urgent but must not be lost

Findings, debts and decisions that are real but not blocking. Without a home, these live in
someone's head and die with the session that noticed them.

⭐ **Rotate the FILE, not the item.** An item opened in January may still be open in December;
what rotates is the file that contains it, on a fixed period. **The item is carried forward until
it closes** — a rotation that closes items by date is a rotation that hides debt.

### 3 · The logbook — history, in order

What happened over time, appended. It is not read at startup and does not need to be small: it is
consulted when someone asks *"why is it like this?"* and the answer is older than the brief.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| where work stopped and what comes next | the work itself — that is `work/blocks/` |
| an item that must outlive this session | a decision already taken — that is an ADR in `rules/` |
| history, appended in order | 🤖 anything a script can measure — that is `docs/` |
| the criterion of the four architects (`principles/`) | ⛔ **any credential** — that is `secrets/` |
| closed material worth consulting (`archive/`) | anything disposable — that is `cache/` |

⚠️ **The line against `work/blocks/`:** a block holds **one** piece of work with its contract and
its state. Memory holds what is true **across** blocks. If the note only matters while one block
is open, it belongs in that block — and it will be archived with it, which is correct.

⚠️ **The line against `docs/`:** if a script could measure it, a script must. A number written
here by hand is correct exactly once, and this is the folder people trust most.

---

## The subfolders

| Folder | Holds | Travels? |
|---|---|---|
| `principles/` | ⭐ the voice and the three architects — **engine doctrine** | ✅ **yes**, whole |
| `archive/` | closed material, kept for consultation | ⛔ instance |

⭐ **`principles/` is the exception inside this folder, and it is deliberate.**

It holds the voice (`principles/owner-0-voice.md`), the three architects who judge
(`principles/owner-1-docs.md`, `principles/owner-2-dev.md`, `principles/owner-3-validation.md`),
and the seven disciplines their judgements are made of (`principles/expertise/`). Those files are
doctrine: how the system communicates and with what criterion it judges. They ship identical to
every clone. They live under `memory/` because criterion **is** what must not be forgotten — but
they are governed by the engine, not by the installer. See its own README.

⛔ **Nothing is deleted from `archive/`.** A closed block is consultable experience: the next time
the same question appears, the answer is already written, including the parts that went wrong.

---

## ⚠️ Before you write here — the four questions

1. **Does this need to survive the session?** If not, it belongs in the block, or nowhere.
2. **Which of the three kinds is it?** State, an open item, or history. If it does not fit one,
   it probably belongs in `work/` or `docs/`.
3. **Would a script measure it better?** ⭐ Then let it. Hand-written numbers here are the ones
   most likely to be believed.
4. **Is it true across blocks, or only inside one?** Only inside one → it goes in that block.

---

## ⛔ Why none of this travels

Every file here describes **one installation's work**: where that person stopped, what they still
owe, what they decided along the way. A clone inheriting it would start with someone else's
unfinished business presented as its own state — and the cold-start brief is the file an AI is
guaranteed to read first, so the wrong one contaminates the very first decision of every session.

The folder ships with its README and its structure. **The content is yours and starts empty.**

---

Related: `principles/README.md` (the criterion that ships) · `../work/README.md` (the work
itself) · `../rules/` (the closing routine and the rotation rule) · `../cache/README.md` (what may
be forgotten) · `../.gitignore` (why the content stays).
