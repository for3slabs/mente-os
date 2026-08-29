# CONTRACT · HANDOFF

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every delegation to another agent
**Enforcement:** 🔒 lock — `bin/check-handoff` · ⭐ **and a gate before the delegation runs**
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

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `HND-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · WHAT THE MANIFEST DECLARES

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

## 3 · ⭐ THE WRITE SCOPE — the rule that matters most

⛔ **A specialist writes to exactly two places, both declared:**

| # | Where | ⭐ Rule |
|---|---|---|
| 1 | **its return artifact** | ⭐ always allowed · it is the specialist's own file |
| 2 | **a bounded append** to one coordinator-owned section | ⚠️ **and every entry declares its ceiling** |

⛔ **Everything else is denied by default.**

> ## ⛔ THERE IS NO "THE TASK NEEDED IT" EXCEPTION
> ⭐ **If the scope was wrong, the MANIFEST was wrong.** Fix the manifest and run the handoff
> again — ⚠️ **widening the scope mid-task is how a boundary becomes a suggestion.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-WRT-001` | ⭐ **The write scope is an allowlist — ⛔ everything else denied** | 🔒 | ⚠️ a denylist can never be complete |
| `HND-WRT-002` | ⭐ **A specialist never writes the block's identity, scope or state** | 🔒 | ⛔ see below |
| `HND-WRT-003` | **Every append declares a line ceiling** | 🔒 | ⭐ an unbounded append is an unbounded writer |

> ## 🔴 IDENTITY, SCOPE, CONNECTIONS, STANDARDS, STATE AND DECISIONS ARE THE COORDINATOR'S
> ⛔ **A specialist that rewrites the state it was given is not delegated work — it is a second
> coordinator**, and now two of them disagree about where the work stands.

---

## 4 · THE RETURN ARTIFACT

| Section | ⭐ What goes in it |
|---|---|
| `objective` | ⭐ **restated from the manifest — it proves the specialist read the right one** |
| `work` | what it actually did |
| `findings` | ⭐ what it found, **with evidence** |
| `open-questions` | ⚠️ what it could not resolve |
| `status` | ⭐ `done` · `blocked` · **`aborted-binding-mismatch`** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-RET-001` | **Every section present, in order** | 🔒 | ⛔ a missing section is an answer nobody asked for |
| `HND-RET-002` | ⭐ **`status` is machine-readable** | 🔒 | ⚠️ prose cannot be dispatched on |

> ## ⭐ `aborted-binding-mismatch` IS THE GOOD FAILURE
> ⛔ It means the specialist found the disk did not match its manifest **and stopped before
> acting.** ⚠️ **A specialist that adapts to a mismatch is a specialist working on something
> nobody asked for.**

---

## 5 · BINDING CHECKS — the manifest against reality

⛔ **Run in order. The first failure aborts, and nothing is written.**

| # | Check | ⛔ Fails when |
|---|---|---|
| 1 | the block path resolves | ⚠️ it is not a directory |
| 2 | the block file exists and is readable | it is missing |
| 3 | ⭐ **the block's declared id matches the manifest** | ⚠️ **the folder was renamed and the manifest was not** |
| 4 | every required read path resolves | one of them moved |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `HND-BND-001` | ⭐ **The checks run in this order** | 📖 | ⛔ see below |
| `HND-BND-002` | **A failed binding aborts before any action** | 🔒 | ⚠️ nothing is written on a mismatch |

⚠️ **Why the order matters:** ⭐ **checking the id before checking the file exists produces a
confusing error instead of the real one.** Each check assumes the previous one passed — ⛔ and a
misleading error costs more than a missing one, because it sends the reader the wrong way.

---

## 6 · ⭐ THE GATE — this is enforced, not suggested

⭐ **The level was measured, not chosen:**

| The specialist can… | Level | ⭐ Why |
|---|---|---|
| ⛔ **WRITE** — including **unknown types** | 🔴 **BLOCK** | an unbounded writer inside a bounded system is the real risk |
| **only READ** | ⚠️ **WARN** | ⭐ it cannot corrupt anything — **and this is the cheap delegation that was missing** |

> ## 🔴 AN UNKNOWN AGENT TYPE FAILS CLOSED
> ⭐ **An agent whose tools are not known could be anything, so it is treated as a writer.**
> ⛔ **Failing open here would make the gate decorative.**

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

## 7 · ⭐ WHEN A HANDOFF IS WORTH IT

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

## 8 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **no manifest** | ⛔ an unbounded agent inside a bounded system |
| ⭐ **no stop condition** | ⚠️ **it runs until the context collapses** |
| **the specialist writes the state** | ⛔ ⭐ **two coordinators disagreeing about where the work stands** |
| **widening the scope mid-task** | ⚠️ the boundary becomes a suggestion |
| **an unknown agent type allowed through** | ⭐ the gate is decorative, and looks exactly like a working one |

---

## 9 · WHO GOVERNS THIS FILE

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
