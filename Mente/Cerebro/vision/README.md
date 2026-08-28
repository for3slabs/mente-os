# Cerebro/vision/ — where the project is going

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the content never does.
**Governance:** `owner` in `piezas.tsv`

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── Cerebro/         ← ⭐ your project's own thinking — what it IS
    ├── ARQUITECTURA.md   the pillar · the ground · must be true NOW
    └── vision/      ← ⭐ YOU ARE HERE — where it is GOING · a dated hypothesis
```

👉 **Read `../README.md` first** if you have not. It explains why `Cerebro/` is the one folder
about your project rather than about the engine, and what the architecture pillar is.

> ## ⭐ THE DISTINCTION THAT SPLIT THESE TWO
> **The pillar describes what IS. This folder describes what MIGHT BE.**
>
> They are separated because they are **trusted differently**. The pillar is the ground: if it and
> the code disagree, one is a bug. A vision document is a hypothesis with a date, and it is
> **allowed to be wrong** — that is not a defect, it is what makes it useful.

⚠️ **Mixed together, both degrade.** The pillar fills with aspiration and stops being reliable
ground; the vision gets read as a commitment nobody actually made.

---

## What this folder is

Documents about direction: where the project is headed, what it could become, what was learned
that changes the course. Explorations, positioning, hypotheses.

⭐ **It is the only folder in the system where being wrong is acceptable** — as long as the
document says when it was written and what it assumed. Everywhere else, an unverified claim is a
defect. Here, an unverified claim clearly marked as a hypothesis is the whole point.

---

## ⛔ THE ONE RULE: every document carries its date and its assumptions

```markdown
**Written:** <date> · **Status:** hypothesis | validated | superseded
**Assumes:** the conditions under which this holds
```

⭐ **A vision document with no date is the most convincing kind of wrong document.** It was
accurate when it was written; the world moved; nothing on the page says so. Six months later it
reads as current, and someone plans around it.

**The three states, and what each means:**

| Status | Means | What to do with it |
|---|---|---|
| **hypothesis** | plausible, not verified | treat as a direction, never as a fact |
| **validated** | something confirmed it | ⭐ **the conclusion probably belongs in the pillar now** |
| **superseded** | reality went elsewhere | ⛔ keep it — see below |

⛔ **A superseded vision is not deleted.** Why the project did *not* go a certain way is expensive
knowledge, and without the record the same idea comes back every few months looking new.

---

## ⭐ WHEN A VISION GRADUATES

A hypothesis that gets confirmed **stops belonging here**:

```
vision/  (hypothesis)  ──validated──►  the pillar, or a decision record
     │
     └── the original document stays, marked validated, pointing at where the conclusion lives
```

⚠️ **The conclusion moves; the document does not.** Two copies of the same claim in two folders
drift apart, and the day they disagree neither is marked wrong. **Name the source, never copy the
value** — the same rule that governs live numbers.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| where the project could go | ⛔ what it **is** — that is the pillar, one level up |
| a hypothesis, dated and marked | a decision already taken — that is a decision record |
| what field experience changed | a plan to execute — that is `docs/plans/` |
| positioning and direction | a unit of work — that is `work/blocks/` |

⚠️ **The line against `docs/plans/`:** a vision says *where* and *why*; a plan says *how* and *in
what order*. A vision document that starts listing steps has become a plan in the wrong folder —
and plans are validated against execution, while visions are not validated at all.

---

## ⚠️ Before you write here — the four questions

1. **Is this what is, or what might be?** What is → the pillar. Even a well-supported guess is
   still a guess, and the pillar has no room for guesses.
2. **What date and what assumptions?** ⭐ Without both, it cannot be re-evaluated later — and
   an unre-evaluable document is read as permanently true.
3. **What would confirm or kill it?** A hypothesis with no test never graduates and never dies;
   it just accumulates.
4. **Has it already been validated?** Then the conclusion goes to the pillar, and this document
   points at it.

---

Related: `../README.md` (⭐ **the parent — read it for context**) · `../ARQUITECTURA.md` (what IS,
where a validated vision graduates to) · `../../docs/README.md` (plans and dated analysis) ·
`../../rules/README.md` (decision records) · `../../.gitignore` (why this stays).
