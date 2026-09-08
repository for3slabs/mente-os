# CONTRACT · INSTALL ORDER

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every step `bin/init` performs, and the order it performs them in
**Enforcement:** 🔒 lock — `bin/probes/probe-init.py` ㉝
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/init` (`prove_gates`) · `bin/probes/probe-init.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## Purpose

⭐ **Installing is a SEQUENCE, not a set of tasks.** Each step depends on what the
one before it wrote, and one step run early writes into a file that does not
exist yet — or over one that does.

> ## 🔴 THE FAILURE THIS CONTRACT EXISTS TO PREVENT
> Measured 2026-09-07 on a real Windows install. Every step ran, every step
> reported success, and the system was **dead**: the host runs a hook through
> bash, bash ate the backslashes out of the interpreter path, and all five gates
> answered `command not found`. ⛔ The host calls that a NON-BLOCKING error, so
> they failed **154 times in one session**, `.beats/` stayed empty, and a whole
> project was built ungoverned while `bin/status` said 🟢 ON.

⚠️ **The steps were not wrong. The MISSING step was.** Nothing fired a gate to
see whether it answered, so *wired* and *alive* were indistinguishable — and the
system reported the first while being the second.

---

## 1 · THE ORDER, AND WHY EACH STEP SITS WHERE IT DOES

⛔ **No step may be skipped, reordered or run in parallel.** Each row states what
it depends on; a step run before its dependency does not fail loudly, it
succeeds against the wrong state.

| # | Step | ⭐ Why HERE and not earlier |
|---|---|---|
| ① | **stamp the templates** | nothing else exists yet to write into |
| ② | **fill `{{owner}}` across the engine** | ⚠️ 78 documents carry it · a header reading `Owner: {{owner}}` passes every check while identifying nobody |
| ③ | **append the router import** | ⛔ the one line written outside `Mente/` · APPENDED, never over |
| ④ | **wire the gates** into `.claude/settings.json` | ⛔ after ③, because ⑦ and ⑧ edit the file this writes |
| ⑤ | **wire the git hooks** (pre-push, pre-commit) | git cannot carry them · needs `.git/` to exist |
| ⑥ | **install the skills** | ⛔ never over a skill of theirs with the same name |
| ⑦ | **place and select the voice** | ⚠️ AFTER ④ — selecting a style before the settings file exists creates a SECOND one beside it, and two files at the same level do not merge |
| ⑧ | **declare the hook registry** | ⛔ after ④, because it records where ④ actually wrote |
| ⑨ | **harden `secrets/`** | last of the writes · ⬜ NOT MEASURED where the platform has no modes |
| ⑩ | 🔴 **FIRE EVERY GATE** — `prove_gates()` | ⭐ **the switch** · everything above must already be on disk, or it proves nothing |

⭐ **⑩ is the only step that MEASURES instead of writing.** The nine before it
report what they did; this one reports whether any of it is real.

---

## 2 · ⭐ THE SWITCH — the rule that gives this contract its name

> ## 🔒 A gate is not installed until it has ANSWERED once.

⛔ **Counting the wiring is not measuring the gate.** `bin/status` counted
entries in a JSON file and printed 🟢; every one of those entries pointed at an
interpreter the shell could not find.

⭐ **So the switch fires each gate exactly as the host will** — through the
shell, with the literal command string from the file just written, and a payload
that names nothing so no gate has cause to refuse. ⚠️ The question is *does it
RUN*, never *does it block*.

| Answer | ⭐ What it means | What the install says |
|---|---|---|
| exit ≠ 127 | the gate ran and decided | `✅ all N gate(s) answered when fired` |
| exit 127 · `command not found` | 🔴 wired and dead | 🔴 names every dead gate |
| the shell itself is missing | ⬜ NOT MEASURED | says so — ⛔ never a silent pass |

### ⛔ AND IT NEVER FAILS THE INSTALL

🔴 A dead gate is reported **loudly** and the run continues. ⚠️ Refusing to
install because a hook is unhappy leaves the person with nothing at all
(`decisions/ADR-012-few-gates-block-the-rest-warn.md`), and a person with nothing cannot even read the
diagnosis.

---

## 3 · ⚠️ QA BEFORE SPEED — the ordering principle, stated by the owner

> *"The hooks must load first, and only THEN start talking. Like a guard and a
> security filter: we wait. It is quality assurance before initial speed."*
> — measured decision, 2026-09-07

⭐ **Two or three seconds at install buys the only moment the system can prove
itself before somebody trusts it with real work.** ⛔ Every second saved by
skipping ⑩ is paid back as a session that believed it was governed.

| ⛔ Never | ⭐ Instead |
|---|---|
| report a step by what it ATTEMPTED | report what it MEASURED |
| treat wiring as coverage | fire it once and read the answer |
| skip ⑩ because the install "looked fine" | 🔴 it looked fine on the machine where everything was dead |
| run ⑩ before ①–⑨ | it would prove a tree that is not there yet |

---

## 4 · THE RULES, and what enforces each

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INS-ORD-001` | ⭐ **The ten steps run in this order** | 🔒 | `probe-init` reads `main()` and asserts the sequence |
| `INS-ORD-002` | ⭐ **⑩ runs LAST and fires every wired gate** | 🔒 | `probe-init ㉝` |
| `INS-ORD-003` | ⛔ **A dead gate is NAMED, never counted** | 🔒 | `probe-init ㉝b` |
| `INS-ORD-004` | ⛔ **⑩ never fails the install** | 🔒 | `probe-init ㉝c` |
| `INS-ORD-005` | ⭐ **`bin/status` fires before it claims green** | 🔒 | `probe-onoff` |

---

## 5 · ⬜ WHAT THIS CONTRACT DOES NOT COVER

⛔ **Said out loud, because a contract silent about its edges reads as covering
them.**

- ⬜ **Whether the host RELOADS the wiring.** Measured 2026-09-07: the session
  had started before the install, so the host never picked the gates up at all.
  ⚠️ That is the host's lifecycle, not this engine's — the install cannot fix it
  and must not pretend to. ⭐ What it CAN do is say the setup is complete and
  the session needs restarting, which `§4c` of `START-HERE.md` covers.
- ⬜ **Whether the assistant OBEYS a gate's refusal.** A refusal is exit 2; what
  happens next is the host's.
- ⬜ **The order of anything after the install.** That is `rule-shipping.md`.

---

## 6 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ adding a step, or what a step writes | whoever maintains the engine, through a recorded decision |
| ⭐ **moving ⑩ out of last place** | **nobody** — ⛔ it would prove a tree that is not finished |
| ⛔ making ⑩ FAIL the install on a dead gate | **nobody** — ⚠️ a person left with nothing cannot read the diagnosis |
| ⛔ reporting a step by what it attempted | **nobody** — 🔴 that is the failure this contract was written from |
| ⬜ how long the switch may take | ⭐ the owner of the instance — QA before speed is the default, not a limit |

---

Related: `../bin/init` (the sequence itself) · `decisions/ADR-012-few-gates-block-the-rest-warn.md`
(a gate that fails closed locks the person out) · `rule-checks-must-measure.md`
(`CHK-CAU-003` — ⬜ said out loud) · `../START-HERE.md` §4c (showing them it is on).
