---
name: session-wrap
description: >- 
  Curated session close for Mente OS. Use whenever the user is closing a working session or about to reset context — "vamos a cerrar", "cerrar sesión",
  "guardar y limpiar","ya acabé por hoy", before a `/clear`, or when a session is about to be compacted. It does the  judgment work no  validator can do: synthesize 
  what mattered , write the session autopsy into the session registry, refresh RETOMAR.md, save memories, update the active block, and only then confirm the cut is safe. Invoke proactively when the user signals a session boundary, even if they do not use the word "wrap".
---
# session-wrap - the curated half of closing a session
`bin/check-clear-ready` is the **deterministic half**: it refuses the cut while something would be lost. This skill is the **curated half** — deciding *what mattered*,
which no script can do.
> **Why it exists:** sessions that end without being registered get lost, and 
> auto-compactions written by a model but reviewed by no one accumulate silently.
> A rule that says "register the session" does nothing on its own —
> **writing the rule does not execute it.** This skill exists to execute the close,
> not just document that it should happen.
>
> Live metrics for this installation (registered sessions, heavy unregistered ones)
> belong in `docs/METRICS.md`, never hardcoded here. (`sessions.registered` · `sessions.heavy_unregistered`).
Work the steps in order. Each is conditional - **skip what does not apply and say what you skipped and why.** This is a wrap, not a session.

---
## Step 0 · Orient

```bash
Mente/bin/check-clear-ready          # what would be lost right now
Mente/bin/check-health               # is anything red
```
Identify the live session and measure it — never estimate:

```bash
ls -t ~/.claude/projects/*/*.jsonl | head -1
```
Size, turns, peak context and tokens come from that `.jsonl` (the `usage` fields of the assistant messages). **A number you did not measure does not go in the autopsy.**

If a block is active, read its `§A-E`.

---

## Step 1 · Synthesize — the judgment
From the actual conversation, distill honestly and briefly:
- **Decisions** taken, and the *why* (the why is what stops a future session re-litigating them).
- **Findings / lessons** — non-obvious things discovered.
- **Bugs** found or fixed, and **mistakes made** — especially method mistakes worth not repeating.
- **Commitments / open items** — what is promised or pending.
**Do not pad.** A session with one real decision gets one line. This feeds Steps 2-5.

> ⚠️ Report what was measured. If something was not verified,  it goes in as *"not verified"* —
> the autopsy is evidence, not a summary of intentions.

---

## Step 2 · 🔴 The session autopsy — mandatory, first
the session registry declared by your instance. **This is the one step that never gets skipped**
(`rules/rule-session-close.md`). Two writes:

1. **A row in the index** — `| S<N> | id | start | end | size | turns | peak ctx | verdict |`
2. **Its autopsy section** — topics · what was done · consumption · **when consumption started
   growing abnormally** · anything strange · reason for closing.

Thresholds (calibrated with real data):

| Signal | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| `.jsonl` size | <15 MB | 15-50 | >50 |
| Live context | <200K | 200-500K | **>500K** |
| Session age | hours | 1-2 days | **days without `/clear`** |

> Observed pattern: sessions tend to die of **AGE, not size** — long-running sessions left open
> for days go red on context well before they ever approach the size limit. Age is the signal
> that matters most. Per-installation evidence lives in `docs/METRICS.md` (`sessions.registered` · `sessions.heavy_unregistered`) , not here.

---
## Step 3 · RETOMAR.md — the cold-start brief

`Mente/memory/RETOMAR.md`. It is the **only** file the next session is guaranteed to read.

- Update **§5 estado actual + próximo paso**. This is the part that decides whether the next session starts working or starts asking.
- **One date, in the header.** Two conflicting dates is a known failure mode.
- **≤200 lines**, enforced by `check-health`. If it grew, move history to `memory/Bitacora_Progreso.md` — not here.
- **Do not write a number that changes on its own.** The battery score was frozen here once and
  went stale within hours — it includes `check-clear-ready`, which measures the *live* session.
  Point at `docs/METRICS.md` instead. **Write the rule, not the snapshot.**

---

## Step 4 · Memories + pending

- **Memories** (`~/.claude/projects/*/memory/`): one fact per file, plus its line in `MEMORY.md`. Prefer **updating** an existing memory over creating a near-duplicate. Only what will matter in *future* conversations — not what the repo or git already records.
- **`Mente/memory/PENDIENTES.md`**: non-urgent findings that should not be lost.

---

## Step 5 · The active block

If a block is open (`Mente/work/blocks/active/*/BLOCK.md`):

- **§E State** — `phase` · `next` · `blockers`, current as of today.
- **§G Decisions** — the load-bearing ones from Step 1, each with its why.
- **§J Context** — consolidated, curated. **Not a log.**

```bash
Mente/bin/check-sufficiency <block>    # can it be restarted from disk alone?
Mente/bin/grade-block <block>          # product or MVP — measured, not opinion
```
> A block that fails sufficiency **does not close**, even if the code works.

---

## Step 6 · Verify, then offer the cut

```bash
Mente/bin/test-f0-f6                   # the whole system — must end with 0 failed
Mente/bin/generate-metrics             # republish the live numbers
Mente/bin/check-clear-ready            # must be green
```

⚠️ **The battery reads one check short until this session is registered** — it includes `check-clear-ready`, which measures the *live* session, so Step 2 is what turns it green. One short right after a `/clear` is **expected, not a regression**.

> 🚫 **Do not write the count into this file.** The current value lives in `docs/METRICS.md`
> (`battery.checks`), regenerated from a real run. A hardcoded count goes stale silently — the
> file keeps a number the battery has already moved past. **Cite the metric, never the number.**

`generate-metrics` re-measures and republishes `docs/METRICS.md`, so every document that points at a metric is current the moment the session closes  — **without anyone remembering to update a number.**

Do **not** commit unless the user asks. Surface what changed and let them decide.

Close with **one** AskUserQuestion:
- **`/clear` (fresh start)** — recommend it when the work reached a natural boundary and Steps 1-5 captured it. It is safe *because* those steps just persisted everything.
- **Continue** — recommend it when mid-task with hot context worth keeping.

**Make the call, then let the user decide.**

---

## Notes
- This skill orchestrates existing pieces — it replaces neither the validators nor the hooks.
- Everything it writes lives on disk, so it survives the cut. That is the whole point:
  **`/clear` is a cut, not a save.**