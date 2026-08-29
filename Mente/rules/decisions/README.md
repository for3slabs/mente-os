# rules/decisions/ — the record of what was already decided

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — ⭐ the folder and this README travel; ⛔ **the records never do.**
**Enforcement:** 🔒 lock — `bin/check-decisions`

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── rules/         ← the law: contracts, rules, decisions
    └── decisions/ ← ⭐ YOU ARE HERE · append-only · ⛔ starts EMPTY
```

👉 **Read `../README.md` first**, and `../contract-adr.md` for the shape of a record.

---

## What a decision record is

⭐ **A photograph of a choice at the moment it was made** — with the problem that forced it, what
was rejected, and how to undo it.

> ## ⭐ ITS VALUE IS NOT THE DECISION. IT IS THAT NOBODY RE-ARGUES IT.

⚠️ **A record is read exactly twice:** once when somebody disagrees with it, and once when
somebody is about to undo it. ⭐ **The second reader is why every record carries `Reverting`.**

---

## ⛔ THIS FOLDER IS APPEND-ONLY

| | |
|---|---|
| ✅ **add** a new record | always |
| ⛔ **edit** an accepted record | ⭐ **never** — supersede it |
| ⛔ **delete** a record | ⚠️ not even one that turned out wrong |
| ⛔ **reuse** a number | ⭐ something cites it |

> ⭐ **The pair — a decision that turned out wrong and its correction — is more useful than a
> clean record that hides that the reasoning ever moved.**

---

## ⛔ Why it starts empty

⭐ **Another installation's decisions are not yours.** A clone inheriting them would start with
somebody else's settled questions presented as its own — ⚠️ **and those are exactly the questions
it should be answering for itself.**

**What travels is the shape. What fills it is yours.**

---

## ⚠️ Before you write one

1. ⭐ **Is this a decision, or a rule?** A decision records *why*; a rule states *what must
   happen*. ⛔ A rule is born from a decision and points back at it.
2. **What was rejected?** ⭐ A record with no rejected alternative cannot be re-examined.
3. ⭐ **What is the evidence?** A number, a file, a command — ⛔ or the words admitting there is
   none. **Silence and an honest "no data" look identical afterwards.**
4. ⚠️ **How is it undone?** ⭐ And if it cannot be, that is the most important sentence in it.

---

Related: `../contract-adr.md` (⭐ **the shape, field by field**) · `../README.md` ·
`../../bin/check-decisions` (what enforces it).
