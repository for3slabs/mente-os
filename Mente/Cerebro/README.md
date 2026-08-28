# Cerebro/ — your project's own thinking

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the content never does.
**Governance:** `owner` in `piezas.tsv`

---

## What this folder is

The only folder in Mente OS that is about **your project** rather than about the engine.
Everything else here describes the tool: how work is governed, verified and remembered. This
describes **what you are building** and **why**.

```
Cerebro/
├── ARQUITECTURA.md   ⭐ the architecture pillar — the ground everything is built on
├── vision/           where the project is going, as opposed to what it is
└── (the project's own records: its history, its decisions in the large)
```

⭐ **It ships empty on purpose.** The engine cannot guess what you are building, and a folder
arriving with somebody else's architecture inside would be worse than an empty one: the AI would
build against it and sound certain doing so.

---

## ⭐ THE ARCHITECTURE PILLAR — the most important file you will write

The pillar is the **source of truth for the shape of your project**: its components, its
invariants, its limits, and the decisions the rest hangs from.

> ## ⛔ If it is empty, the AI builds by inference — and sounds exactly as confident.
> That is the failure this file prevents. Not a wrong answer delivered with doubt: a wrong answer
> delivered with the same certainty as a right one, because nothing on disk contradicted it.

**Start from the template and fill it as the project takes shape.** It is not written in one
sitting — it is written as decisions get made, and a half-filled pillar already beats none.

⚠️ **It must describe what IS, not what you wish.** ⭐ **When the pillar and the code disagree,
one of them is a bug — and you have to decide which.** A pillar that describes the intention
rather than the reality is worse than no pillar: it gives false confidence to every reader,
including the ones who trust it instead of checking.

### How the engine finds it — no filename is ever hardcoded

```
mente.config.yml  →  pillars.architecture: <path>   ← you point here, once
        ▲                        │
        │ generated from         │ read by
        │                        ▼
   the template          the router + the project rules
                        ("the architecture pillar declared in config")
```

⭐ **No engine file names your architecture file.** They ask config where it is. That is what lets
you call it whatever you want, put it wherever you want, or have several — without editing a
single engine file.

---

## The line against the rest of the system

This is the distinction that decides where a document goes, and it is easy to get wrong:

| Folder | Describes | Example question |
|---|---|---|
| `rules/` | how **the tool** governs work | *"must a block declare its scope?"* |
| `memory/principles/` | with what **criterion** to judge | *"is this scope well written?"* |
| ⭐ **`Cerebro/`** | what **your project** is and why | *"what are the components, and what must never break?"* |
| `docs/` | analysis and plans, dated | *"what did we measure in that investigation?"* |

⚠️ **A rule about your project is not a rule of the engine.** *"Never deploy on Friday"* is
project-level: it belongs to your project rules, not to `rules/`, which travels to everyone.
Getting this wrong is how a clone inherits a constraint that has nothing to do with it.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| the architecture pillar | how the engine works — that is `docs/architecture/` |
| where the project is going (`vision/`) | a unit of work — that is `work/blocks/` |
| the project's own long-form records | a rule of the tool — that is `rules/` |
| the invariants that must never break | 🤖 anything a script measures — that is `docs/` |

---

## `vision/` — the subfolder, and why it is separate

**This folder holds what the project IS. `vision/` holds where it is GOING.**

⭐ **They are separated because they age differently and are trusted differently.** The pillar must
be true right now — it is the ground. A vision document is a hypothesis with a date on it, and it
is allowed to be wrong. Mixing them means either the pillar fills with aspiration, or the vision
gets read as a commitment.

👉 See `vision/README.md`.

---

## ⚠️ Before you write here — the four questions

1. **Is this about the project, or about the tool?** About the tool → it belongs to the engine
   folders and travels to everyone.
2. **Is it what IS, or what you want?** What is → here. What you want → `vision/`.
3. **Is it measured or assumed?** ⭐ A pillar stating something nobody verified is the most
   convincing kind of wrong document.
4. **Does config point at it?** If it is the pillar and config does not name it, nothing will
   ever read it — and its absence is silent.

---

Related: `vision/README.md` (where the project is going) · `../mente.config.yml`
(`pillars.architecture`, which points here) · `../templates/README.md` (the pillar's template) ·
`../rules/README.md` (rules of the tool, not of your project) · `../.gitignore` (why this stays).
