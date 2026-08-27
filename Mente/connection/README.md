# connection/ — everything that reaches outside this installation

**Status:** current · **Type:** folder-readme
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the content never does.
**Governance:** `owner` in `piezas.tsv`

---

## What this folder is

The **outward-facing edge** of an installation. Everything else in Mente OS looks inward: the
work, the rules, the memory, the project's own thinking. This is where the system deals with what
is **not** itself — other installations, other trees, anything an agent could read but should not
read casually.

```
connection/
└── bridges/     🌉 the gate to other Mente OS installations
```

> ⭐ **The folder is named after the FUNCTION, not after a tool.** What lives here may change —
> bridges today, other connectors later — but the question it answers does not: *what is outside
> this installation, and under what rule may it be reached?* A folder named after whatever
> happened to be built first has to be renamed the moment a second thing arrives.

---

## ⭐ WHY REACHING OUTSIDE NEEDS A FOLDER AT ALL

Reading is not free, and that is the part people underestimate.

| | Reading inside this installation | Reading another one |
|---|---|---|
| Cost | bounded — the engine keeps files small on purpose | ⭐ **unbounded** |
| Relevance | it is your work | it is somebody else's |
| Who decides | the task | ⛔ **must be a person** |

⛔ **The failure this prevents:** an agent that reads another installation *"for context"* or
*"just in case"* pulls in an entire second system — its rules, its state, its history — most of
which has nothing to do with the task. The cost lands immediately; the benefit is speculative.

⭐ **And it is not only cost. It is contamination.** Another installation's rules and state are
true *there*. Loaded here, they get applied here — and nothing marks which half of the resulting
context came from somewhere else.

---

## The rule this folder implements

> ## Point at it. Do not integrate it.
> This installation may know that another exists and where it lives. It does not read it until a
> person says so, with a stated reason.

⚠️ **Declaring a connection is not granting access.** The registry here says *what exists*; the
configuration declares *what is gated*; the harness is what actually refuses. Three separate
things — and only the last one stops anything.

⭐ **A gate written only in a document gets violated.** That is the measured base rate for
document-only rules, and this is a rule where each violation costs real money and real accuracy.
The registry documents; the technical deny enforces. **Never treat the document as the lock.**

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| the registry of other installations and their gates | ⛔ **a copy of anything from them** |
| the rule for how access is requested and closed | credentials to reach them — that is `secrets/` |
| what this installation may expose outward | your own work — that is `work/` |

⚠️ **The line against `secrets/`:** this folder says *which* systems exist and under what rule.
`secrets/` holds *how* to reach one. Never merge them — a registry is meant to be read easily,
and a credential is meant not to be.

⛔ **Never cache content from another installation here.** A copy of somebody else's state is
stale from the moment it is written, and it is read as if it were current. If you needed it, open
the gate again and read the source.

---

## `bridges/` — the subfolder

Holds the registry of other Mente OS installations and the rules for reaching them: which exist,
why they are separate, the phrase that opens access, and what closes it.

👉 See `bridges/README.md` for the mechanism.

---

## ⚠️ Before you add anything here — the three questions

1. **Is this about something outside this installation?** If it is internal, it belongs to one of
   the inward folders.
2. **Is it a pointer or a copy?** ⭐ Pointers only. A copy is a second source of truth that nobody
   updates.
3. **Is the corresponding gate declared in config?** A registry entry with no technical gate
   behind it is documentation of a limit that does not exist.

---

Related: `bridges/README.md` (🌉 the gate and how it opens) · `../mente.config.yml` (`gates:`,
where the enforceable declaration lives) · `../secrets/README.md` (how to reach things, never
what) · `../CAPABILITIES.md` §4 (what must not be touched) · `../.gitignore` (why this stays).
