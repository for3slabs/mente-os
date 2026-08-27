# connection/bridges/ — 🌉 the gate to other Mente OS installations

**Status:** current · **Type:** folder-readme
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the registry never does.
**Governance:** `owner` in `piezas.tsv`

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── connection/      ← everything that reaches OUTSIDE this installation
    └── bridges/     ← ⭐ YOU ARE HERE · the gate to other Mente OS installations
```

👉 **Read `../README.md` first** if you have not. It explains why reaching outside needs its own
folder at all — the cost, the contamination, and the rule *point at it, do not integrate it*.
This file is the mechanism that rule runs on.

---

## What this folder is

The **registry of other Mente OS installations** this one may point at, and the rules for reaching
them. A bridge is one entry: which installation, where it lives, why it is separate, and what
opening it requires.

> ## ⛔ THE HARD RULE
> **Never read another Mente OS unless a person explicitly asks, with a stated reason.**
> Not "for context". Not "to understand better". Not "just in case".

⭐ **A second installation is a whole second system** — its rules, its state, its history, its
work. Opening one is not reading a file; it is loading somebody else's entire world into a
session that was working on yours.

---

## Why the rule is this strict — two costs, and the second is worse

| Cost | What happens |
|---|---|
| **Consumption** | reading a full installation is expensive, and the expense is immediate while the benefit is speculative |
| ⭐ **Contamination** | its rules and its state are true **there**. Loaded here, they get applied here — and nothing marks which half of the context came from elsewhere |

⚠️ **Contamination is the one that is hard to notice.** An expensive read is visible. An agent
quietly applying another project's constraints to yours produces confident, well-reasoned, wrong
work — and the reasoning looks sound because it *is* sound, for the other project.

---

## ⭐ HOW A BRIDGE OPENS AND CLOSES

```
CLOSED  ──── a person states the access phrase + WHY ────►  OPEN
   ▲                                                          │
   │                          read-only · report back         │
   └──── explicit close, OR the task ends, whichever first ◄───┘
```

**Four properties, and each exists for a reason:**

| Property | Why |
|---|---|
| **A person opens it** | ⛔ never the agent, never "it seemed useful" |
| ⭐ **A stated WHY** | forces the question *do I actually need this?* — most of the time the answer is no |
| **Read-only** | you are a guest in a tree with its own rules; writing there breaks a system you are not governing |
| **Auto-closes with the task** | ⭐ an access that outlives its reason becomes a permanent one nobody decided to grant |

---

## ⭐ THE REGISTRY IS NOT THE LOCK

This is the most important distinction in this folder, and the easiest to get wrong.

```
bridges/     documents WHICH installations exist and why      📖 a document
config       declares which trees are gated                   📋 a declaration
the harness  actually refuses to read them                    🔒 the lock
```

⛔ **Only the third one stops anything.** A registry entry with no technical gate behind it
documents a limit that does not exist — and it reads exactly like one that does.

⭐ **The measured reason this matters:** a rule enforced by code is followed every time; a rule
that lives only in a document is followed roughly half the time. A gate that existed only as an
agreement is precisely the kind that gets crossed repeatedly in a single session, each time for a
reason that seemed good in the moment.

⚠️ **So the registry and the configured gates must agree.** If they diverge, the configuration is
what happens and the document is a claim. Keep them in sync, and when in doubt, trust the lock.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| an entry per external installation: where, why separate, how to open | ⛔ **any content copied from one** |
| the phrase that opens and what closes it | credentials to reach it — that is `secrets/` |
| what was read, and why, if you keep a record | your own work — that is `work/` |

⛔ **Never cache another installation's content here.** It is stale the moment it is written and
read as if it were current. If you need it again, open the gate again.

---

## ⚠️ Before you register a bridge — the four questions

1. **Why are these separate installations?** If there is no good answer, they may be one — and a
   bridge is not a fix for a split that should not exist.
2. **What does opening it require?** Write the phrase and the closing condition. A gate with no
   stated way to open it gets bypassed rather than requested.
3. **Is the gate declared in config?** ⭐ Without it, this entry is documentation, not protection.
4. **What is the smallest thing you would need to read?** A bridge that always means "read
   everything" is a bridge that will stop being opened at all — and then it gets bypassed.

---

## ⛔ If you are the agent reading this

You may **know** these installations exist. You may **point** at them. You may **not** read them
until asked, with a reason.

⭐ **If you think you need one: say so and stop.** Explain what you would look for and why. The
person decides. Reading first and reporting afterwards is not initiative — it is spending
somebody else's resources on a guess, and there is no way to take it back.

---

Related: `../README.md` (⭐ **the parent — read it for context**) · `../../mente.config.yml`
(`gates:` — the declaration that becomes the lock) · `../../CAPABILITIES.md` §4 (what must not be
touched) · `../../secrets/README.md` · `../../.gitignore` (why the registry stays).
