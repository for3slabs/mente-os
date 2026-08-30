# CONTRACT · HANDOFF

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every delegation to another agent
**Enforcement:** 🔒 lock — `bin/check-handoff` · ⭐ **and a gate before the delegation runs**
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-handoff` · `bin/probes/probe-handoff.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ A written contract between a coordinator and a specialist: what it may read, what it must do, where it may write, and when it must stop.

⚠️ **Delegating is not the problem. Delegating with no bounds is.** ⛔ A specialist spawned with
no declared scope reads whatever it wants, writes wherever it lands, and returns prose nobody can
verify — ⭐ **and the cost lands back in the coordinator's context, which is exactly what
delegation was meant to avoid.**

> ## 🚫 NO MANIFEST, NO DELEGATION.
> ⛔ **A specialist with no declared write scope is an unbounded agent inside a bounded system.**

### ⭐ THE MEASUREMENT THAT INVERTED THE DIAGNOSIS

⚠️ **Counting the actual tool calls across a project's history showed something unexpected:**
⭐ **shell and file operations in the thousands; delegations in the dozens — and half of those
read-only.**

> ## ⭐ THE FAILURE WAS NOT DELEGATING BADLY. IT WAS NOT DELEGATING AT ALL.
> ⚠️ There was no history of specialists writing where they should not. ⛔ **There was a history
> of everything happening in one context until it collapsed.**

⭐ **That is why this contract bounds writing hard and leaves reading cheap** — the risk and the
missing behaviour are not the same thing.

---

## 1 · ⭐ WHAT A HANDOFF ACTUALLY IS

> ## ⭐ Not an instruction to another agent — a TEMPORARY, VERIFIABLE, LIMITED GRANT OF AUTHORITY.

⚠️ **The difference is not wording.** ⭐ An instruction is obeyed as well as it
is understood; ⛔ **a capability is bounded whether it is understood or not.**

```
the specialist receives:   identity + READ capability + task
                         + WRITE capability + stop conditions
                                    ⛔ and nothing else
when it finishes:          the capability EXPIRES
                           the result is VALIDATED
                           control returns to the coordinator
```

### ⭐ THE TEN INVARIANTS — ⛔ never broken, whatever the task needs

| # | A specialist MUST… |
|---|---|
| 1 | ⭐ **validate the handoff BEFORE reading any task file** |
| 2 | read only what `load` allows |
| 3 | ⭐ **write only where `write_back` allows** |
| 4 | ⛔ **never modify coordinator-owned state** |
| 5 | stop the moment a binding check fails |
| 6 | stop when its stop condition is met |
| 7 | ⭐ **never expand its own scope** |
| 8 | return the declared artifact shape |
| 9 | ⭐ **report uncertainty instead of inventing** |
| 10 | ⛔ **never treat task necessity as permission** |

⭐ **Invariant 10 is the one that gets rationalised away**, and §5 is the whole
argument for it.

---

## 2 · ⭐ WHO MAY DO WHAT

| Action | Coordinator | Specialist |
|---|---|---|
| create the handoff | ✅ | ⛔ |
| ⭐ **define the scope** | ✅ | ⛔ |
| validate the manifest | ⭐ the system | ⭐ the system |
| read what `load.required` names | ✅ | ✅ |
| ⛔ **read outside `load`** | ✅ | ⛔ **never** |
| ⛔ **change identity, scope, state or decisions** | ✅ | ⛔ **never** |
| write the return artifact | — | ✅ |
| append to the one allowed section | ✅ | ⭐ bounded |
| ⭐ **change the scope mid-task** | ✅ ⚠️ by reissuing | ⛔ **never** |
| decide what the result means | ✅ | ⛔ |

> ## ⭐ THE SPECIALIST EXECUTES WITHIN THE COORDINATOR'S AUTHORITY.
> ⛔ **It does not acquire authority by discovering information.** ⚠️ Finding
> out that something else matters is a finding to report — **not a permission
> that just arrived.**

---

## 3 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `HND-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 4 · WHAT THE MANIFEST DECLARES

| Field | Req | ⭐ What it settles |
|---|---|---|
| `schema_version` | 🔴 | ⭐ **a specialist REFUSES an unknown version** rather than guessing at the shape |
| `handoff_id` | 🔴 | unique within the block |
| `block` | 🔴 | ⭐ which block this belongs to — ⚠️ **it must exist on disk** |
| `block_path` | 🔴 | where that block lives |
| `role` | 🟢 | descriptive only, for logs |
| `load` | 🔴 | ⭐ **the READ scope** — `required` plus `optional` |
| `task` | 🔴 | `objective` · `success_condition` · ⭐ **`stop_condition`** |
| `binding_checks` | 🔴 | ⭐ machine-testable, run in order — ⛔ first failure aborts |
| `write_back` | 🔴 | ⭐ **the WRITE scope** — where the return goes, and what it must contain |

> ## ⭐ THE TWO SCOPES ARE THE POINT
> `load` bounds reading. `write_back` bounds writing. ⛔ **Everything else exists to make those
> two verifiable.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-MAN-001` | **Every required field present** | 🔒 | ⛔ a missing field is an unbounded scope |
| `HND-MAN-002` | ⭐ **An unknown schema version is REFUSED, never guessed** | 🔒 | ⚠️ guessing the shape is how a bound becomes decorative |
| `HND-MAN-003` | ⭐ **`stop_condition` is present and observable** | 🔒 | ⛔ *"when done"* is not a stop condition |

⭐ **`HND-MAN-003` is the one people leave vague.** ⚠️ **A specialist with no stop condition runs
until it runs out of context** — which is the failure this whole contract exists to prevent.

---

## 5 · ⭐ THE READ SCOPE — and why needing is not permission

⛔ **`load` is an allowlist. Everything outside it is out of reach**, however
relevant it turns out to be.

| ⛔ A specialist MUST NOT | ⭐ |
|---|---|
| **discover files outside `load`** | ⚠️ a listing is a read |
| ⭐ **scan a directory that `load` does not name** | ⛔ not even to "orient itself" |
| **read a parent directory** | ⭐ the path given is the path allowed |
| ⭐ **follow a reference out of scope** | ⚠️ **a pointer is not a permission** |
| **inspect project-wide state** | ⛔ unless `load` says so |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-RED-001` | ⭐ **Reading outside `load` is a violation, not a shortcut** | 📖 | ⛔ nothing verifies this at runtime |
| `HND-RED-002` | 🔴 **NEEDING A FILE DOES NOT CREATE PERMISSION TO READ IT** | 📖 | ⭐ see below |
| `HND-RED-003` | ⭐ **Out of scope → stop and report, never widen** | 📖 | ⚠️ §8, boundary stop |

> ## 🔴 `HND-RED-002` — the rationalisation this contract exists to stop
> ⚠️ **The specialist discovers it needs something the manifest did not grant.**
> ⭐ **That is a FINDING, not a permission that just arrived.**
>
> ```
> ⛔  "I need this to do the job"  →  reads it
> ✅  "this is outside my scope"   →  BOUNDARY STOP · reported
> ```
>
> ⛔ **The first is how a bounded agent becomes an unbounded one — one
> reasonable step at a time**, and every step looks justified from inside.

⭐ **The way out is a reissued manifest, not a wider reading.** ⚠️ **The cost of
stopping is one round trip. The cost of widening is that the boundary stops
meaning anything.**

---

## 6 · ⭐ THE WRITE SCOPE — the rule that matters most

⛔ **A specialist writes to exactly two places, both declared:**

| # | Where | ⭐ Rule |
|---|---|---|
| 1 | **its return artifact** | ⭐ always allowed · it is the specialist's own file |
| 2 | **a bounded append** to one coordinator-owned section | ⚠️ **and every entry declares its ceiling** |

⛔ **Everything else is denied by default.**

> ## ⛔ THERE IS NO "THE TASK NEEDED IT" EXCEPTION
> ⭐ **If the scope was wrong, the MANIFEST was wrong.** Fix the manifest and run the handoff
> again — ⚠️ **widening the scope mid-task is how a boundary becomes a suggestion.**

### ⭐ AND THE MODE IS PART OF THE PERMISSION

| ⭐ Granted | ⛔ Does NOT mean |
|---|---|
| **create** the artifact | ⚠️ modify one that exists |
| ⭐ **append** to a section | ⛔ **overwrite that section** |
| **a named section** | ⭐ **the whole file** |
| **a named path** | ⛔ its parent directory |
| a line ceiling | ⚠️ ⭐ **a hard limit, not a suggestion** |

> ## ⭐ "I MAY WRITE IN SECTION J" IS NOT "I MAY EDIT THIS FILE."
> ⛔ **Every row above is a widening somebody could argue for**, and each one
> ends with the coordinator's own state rewritten by somebody else.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-WRT-001` | ⭐ **The write scope is an allowlist — ⛔ everything else denied** | 🔒 | ⚠️ a denylist can never be complete |
| `HND-WRT-004` | ⭐ **The MODE is granted, not assumed** | 🔒 | ⛔ create ≠ modify · append ≠ overwrite |
| `HND-WRT-002` | ⭐ **A specialist never writes the block's identity, scope or state** | 🔒 | ⛔ see below |
| `HND-WRT-003` | **Every append declares a line ceiling** | 🔒 | ⭐ an unbounded append is an unbounded writer |

> ## 🔴 IDENTITY, SCOPE, CONNECTIONS, STANDARDS, STATE AND DECISIONS ARE THE COORDINATOR'S
> ⛔ **A specialist that rewrites the state it was given is not delegated work — it is a second
> coordinator**, and now two of them disagree about where the work stands.

---

## 7 · THE RETURN ARTIFACT

| Section | ⭐ What goes in it |
|---|---|
| `objective` | ⭐ **restated from the manifest — it proves the specialist read the right one** |
| `work` | what it actually did |
| `findings` | ⭐ what it found, **with evidence** |
| `open-questions` | ⚠️ what it could not resolve |
| `status` | ⭐ one of the five below |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-RET-001` | **Every section present, in order** | 🔒 | ⛔ a missing section is an answer nobody asked for |
| `HND-RET-002` | ⭐ **`status` is machine-readable** | 🔒 | ⚠️ prose cannot be dispatched on |

### ⭐ THE FIVE OUTCOMES — they send the coordinator to different places

| `status` | Means | ⭐ What the coordinator does |
|---|---|---|
| ✅ **done** | the success condition was met | accept |
| ⭐ **partial** | ⚠️ **part completed and valid; the rest was not** | accept the part, reissue the rest |
| ⚠️ **blocked** | ⛔ it lacked permission or information | ⭐ widen the manifest, or answer |
| 🔴 **aborted-binding-mismatch** | reality did not match the manifest | ⭐ the world moved — re-derive it |
| 🔴 **failed** | ⛔ **it had everything it needed and the work failed** | ⚠️ that is a real defect |

⛔ **Collapsing these is how a coordinator retries the wrong thing.** ⭐ *"I was
not allowed"*, *"the world changed"* and *"I tried and it broke"* need three
different responses.

### ⭐ A FINDING CARRIES ITS EVIDENCE AND ITS CONFIDENCE

```
- claim:      <what was found>
  evidence:   <where — a path, a line, a command, an output>
  confidence: high | medium | low
```

| ⭐ Confidence | Means |
|---|---|
| **high** | ⭐ directly demonstrated by the evidence shown |
| **medium** | strong evidence, ⚠️ incomplete |
| ⭐ **low** | ⛔ **a hypothesis that needs validating** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-FND-001` | ⭐ **Every finding names where it was found** | 🟡 | ⛔ a claim with no location cannot be rechecked |
| `HND-FND-002` | 🔴 **A low-confidence finding is NEVER presented as a fact** | 📖 | ⭐ see below |

> ## 🔴 `HND-FND-002` — the sentence that costs most
> ⛔ **A hypothesis written as a conclusion is indistinguishable from a measured
> one**, and the coordinator acts on both the same way. ⭐ **Confidence is not
> hedging: it is the difference between what was shown and what was guessed.**

> ## ⭐ `aborted-binding-mismatch` IS THE GOOD FAILURE
> ⛔ It means the specialist found the disk did not match its manifest **and stopped before
> acting.** ⚠️ **A specialist that adapts to a mismatch is a specialist working on something
> nobody asked for.**

---

## 8 · ⭐ THE THREE STOPS — and nothing happens after one

| Kind | ⭐ When | What the artifact says |
|---|---|---|
| ✅ **SUCCESS STOP** | the success condition is met | `done` — ⭐ or `partial` |
| ⚠️ **BOUNDARY STOP** | ⭐ **it needs something outside its scope** | `blocked`, ⛔ naming exactly what |
| 🔴 **FAILURE STOP** | ⛔ **reality contradicts the manifest** | `aborted-binding-mismatch` · `failed` |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-STP-001` | ⭐ **A specialist stops the moment a stop condition is met** | 📖 | ⛔ nothing verifies this at runtime |
| `HND-STP-002` | 🔴 **NO FURTHER DISCOVERY AFTER A STOP** | 📖 | ⭐ see below |
| `HND-STP-003` | ⭐ **A boundary stop names exactly what it lacked** | 🔒 | ⛔ *"I could not continue"* is not a report |

> ## 🔴 `HND-STP-002` — the one that is broken with good intentions
> ⚠️ **After stopping, "let me just check one more thing" is reading outside a
> scope that has already ended.** ⭐ **A stop is the end of the capability, not
> a pause in it.**

⭐ **And the cost of the alternative is measured:** ⛔ *"one more look"* is
exactly how a bounded task turns into hundreds of operations whose output
never leaves the context.

---

## 9 · BINDING CHECKS — the manifest against reality

⛔ **Run in order. The first failure aborts, and nothing is written.**

| # | Check | ⛔ Fails when |
|---|---|---|
| 1 | the block path resolves | ⚠️ it is not a directory |
| 2 | the block file exists and is readable | it is missing |
| 3 | ⭐ **the block's declared id matches the manifest** | ⚠️ **the folder was renamed and the manifest was not** |
| 4 | every required read path resolves | one of them moved |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-BND-001` | ⭐ **The checks run in this order** | 🔒 | `bin/check-handoff` · ⛔ the first failure returns, so the order IS enforced |
| `HND-BND-002` | **A failed binding aborts before any action** | 🔒 | ⭐ performed by `HND-BND-001` — the same return, not a second check |

⚠️ **Why the order matters:** ⭐ **checking the id before checking the file exists produces a
confusing error instead of the real one.** Each check assumes the previous one passed — ⛔ and a
misleading error costs more than a missing one, because it sends the reader the wrong way.

---

## 10 · 🔴 POST-FLIGHT — validating what came back

> ## ⛔ VALIDATING BEFORE THE SPECIALIST RUNS IS HALF THE PROBLEM.

⚠️ **The write scope is a promise until something checks it was kept.** ⭐ **A
specialist that wrote outside its allowlist leaves no trace anybody looks
at** — and the coordinator reads the artifact as if the boundary had held.

```
PRE  ──▶ validate the manifest and its binding
WORK ──▶ the specialist runs
POST ──▶ ⭐ validate what it actually did
```

| # | Post-flight check | ⛔ Fails when |
|---|---|---|
| 1 | **the artifact exists** | ⚠️ ⭐ `done` with no artifact |
| 2 | **it belongs to this handoff** | it names another id |
| 3 | ⭐ **its sections match the declared schema, in order** | one is missing or renamed |
| 4 | **`status` is one of the five** | ⛔ free text cannot be dispatched on |
| 5 | ⭐ **only allowed paths changed** | ⚠️ **the write scope was exceeded** |
| 6 | ⭐ **only the allowed section was appended to** | the whole file was rewritten |
| 7 | **the line ceiling was respected** | an unbounded append |
| 8 | ⛔ **no coordinator-owned section changed** | 🔴 a second coordinator |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-PST-001` | ⭐ **A handoff is not complete until post-flight passes** | 🔒 | ⛔ the result is rejected, not accepted-with-notes |
| `HND-PST-002` | 🔴 **`done` requires an artifact that validates** | 🔒 | ⭐ see below |
| `HND-PST-003` | ⭐ **A rejected result is returned, never partially merged** | 📖 | ⚠️ half a bounded result is unbounded |

> ## 🔴 `HND-PST-002` — a claim of completion that nothing backs
> ⛔ **With nothing validating the return, a specialist reporting `done` and
> having done nothing is indistinguishable from one that worked.**
>
> ⭐ **It is the same shape as a decision recorded `accepted` and never
> implemented:** ⚠️ **an assertion of completeness with no evidence behind it,
> and everything downstream treats it as settled.**

---

## 11 · ⭐ THE GATE — this is enforced, not suggested

⭐ **The level was measured, not chosen:**

| The specialist can… | Level | ⭐ Why |
|---|---|---|
| ⛔ **WRITE** — including **unknown types** | 🔴 **BLOCK** | an unbounded writer inside a bounded system is the real risk |
| **only READ** | ⚠️ **WARN** | ⭐ it cannot corrupt anything — **and this is the cheap delegation that was missing** |

> ## 🔴 AN UNKNOWN AGENT TYPE FAILS CLOSED
> ⭐ **An agent whose tools are not known could be anything, so it is treated as a writer.**
> ⛔ **Failing open here would make the gate decorative.**

### ⭐ THE GATE DECIDES ON CAPABILITIES, NOT ON NAMES

```
⛔  is it called one of these three names?
✅  what can it DO?   read: yes · write: yes  →  it is a writer
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-GAT-004` | ⭐ **The level comes from declared capabilities** | 🔒 | ⛔ a name list ages; a capability does not |
| `HND-GAT-005` | ⭐ **An undeclared capability is assumed present** | 🔒 | ⚠️ fail closed, again |

⚠️ **A list of names is the loose comparison of `rule-checks-must-measure.md`
§4-A, in another shape:** ⛔ **it is correct exactly until somebody adds a
fourth agent type** — ⭐ and then the gate is silently permissive for it.

### ⭐ Presence is not compliance

⛔ **A manifest sitting on disk opens nothing.** The gate runs the validator on it and requires a
clean pass. ⚠️ **A malformed or unfilled manifest leaves the gate shut** — ⭐ otherwise the scope
would be paperwork rather than a boundary.

### The escape hatch

⭐ **There is one, deliberately** — ⚠️ **a gate with no escape hatch gets deleted.** It is loud:
it prints that nothing records what the specialist may read, where it may write, or when it must
stop.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-GAT-001` | ⭐ **An unknown agent type is treated as a writer** | 🔒 | ⛔ fail closed |
| `HND-GAT-002` | **The gate verifies the manifest, not its presence** | 🔒 | ⚠️ ⭐ an unfilled template must not open it |
| `HND-GAT-003` | ⭐ **The escape hatch announces itself** | 📖 | ⛔ a silent bypass is a removed gate |

---

## 12 · ⭐ WHEN A HANDOFF IS WORTH IT

> ## ⛔ NOT EVERY TASK DESERVES A MANIFEST.
> ⚠️ **Writing one costs more than a small task saves** — and a contract nobody writes because it
> is too heavy protects nothing.

| ⭐ Delegate | ⛔ Do it inline |
|---|---|
| a broad search where ⭐ **only the conclusion matters** | anything answerable with two reads |
| a bounded sub-task whose intermediate output would flood the context | ⚠️ work needing the coordinator's full context to judge |
| repeated mechanical work over a known set | one-off edits |

⭐ **The measured signal:** ⛔ **if the work would produce dozens of operations whose OUTPUT you do
not need — only the conclusion — that is a handoff.** ⚠️ **The counter-example is a session where
hundreds of operations kept their full output in context forever.**

---

## 13 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **no manifest** | ⛔ an unbounded agent inside a bounded system |
| ⭐ **no stop condition** | ⚠️ **it runs until the context collapses** |
| **the specialist writes the state** | ⛔ ⭐ **two coordinators disagreeing about where the work stands** |
| **widening the scope mid-task** | ⚠️ the boundary becomes a suggestion |
| **an unknown agent type allowed through** | ⭐ the gate is decorative, and looks exactly like a working one |
| ⭐ **reading outside `load` because the task needed it** | ⛔ **a bounded agent becomes unbounded, one reasonable step at a time** |
| **nothing validating the return** | ⭐ `done` with nothing done reads exactly like `done` |
| ⭐ **a low-confidence finding written as a fact** | ⚠️ the coordinator acts on a guess as if it were measured |
| **the gate keyed on names** | ⛔ ⭐ **silently permissive for every type added later** |

---

## 14 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ which agent types exist here, and their tools | ⭐ the owner of the instance |
| the manifest shape and the binding checks | whoever maintains the engine, through a recorded decision |
| ⛔ letting an unknown type write | **nobody** — ⭐ ⚠️ **fail closed is the whole reason the gate means anything** |

---

Related: `README.md` (⭐ the three document types) · `contract-block.md` (⭐ **the block a handoff
binds to — and the only section a specialist may append to**) · `rule-working-in-a-block.md`
(⭐ §3 — isolation, which this extends to a second agent) · `contract-document.md` ·
`../bin/check-handoff` (what enforces the 🔒 rows).
