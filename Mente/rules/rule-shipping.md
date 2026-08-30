# RULE · SHIPPING

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** ⭐ **every discipline** — a change ships the same way whatever it touches
**Enforcement:** 🔒 partial — `bin/check-shipping` · ⚠️ **several rows here are 📖**
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-shipping` · `bin/probes/probe-shipping.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone
**Size:** ⭐ **a BASE file — it ships whole.** See `contract-document.md` §4.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ How a finished change leaves the workspace — and how the session that made it is closed.

⚠️ **The failure it prevents is not a bad change. It is a good change that never arrives**, or one
that arrives and then quietly disappears.

### ⭐ It absorbs five things that used to be separate

| | Why it is here |
|---|---|
| **the loop** — from ticket to reviewable change | the spine |
| **the base** — what a change is proposed against | ⭐ get it wrong and the work is lost |
| **grouping** — how many items per proposal | ⚠️ and when a group closes a block |
| **cleanup** — verify, then delete | ⛔ delete first and the only copy is gone |
| ⭐ **closing the session** | the cut that saves nothing |

⭐ **One owner, one moment.** ⛔ Five files made a reader open five to follow one change from start
to gone.

### ⭐ WHY THIS IS A RULE AND NOT PART OF A DISCIPLINE

⚠️ **Measured, and it is the reason this file exists at this level:** what injects standards
before an edit injects **only what the block declares** — ⛔ **so a shipping flow living inside one
discipline never reaches a block of another.**

⭐ **The flow is transversal. What changes per discipline is WHAT gets verified**, and that lives
in each discipline's own criterion.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `SHP-<area>-<nnn>` — ⛔ never renumbered, never reused.

⚠️ **This file carries the sharpest 📖/🔒 split in the folder**, and the reason is measured — §2.

---

## 2 · 🔴 THE MEASUREMENT THAT MADE THIS A LOCK

⚠️ **A rule of this kind existed, written and readable, and it was followed ZERO out of fifteen
times.** ⛔ **Fifteen of fifteen changes went straight to the base branch** — and a person found
it, not a validator.

⭐ **The battery was green the whole time.** Its check verified that a block **DECLARED** the rule.

> ## ⛔ DECLARING A RULE IS NOT FOLLOWING IT.
> ⭐ **Code is followed 100%; a document 40-60%.** ⚠️ **This one, as a document alone, scored 0.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-LCK-001` | ⭐ **A commit on the base branch is refused, not warned about** | 🔒 | ⛔ the gate blocks; the check watches the gate |
| `SHP-LCK-002` | ⭐ **The escape hatch leaves a trace and is justified** | 📖 | ⚠️ a silent bypass is a removed gate |

⭐ **And it applies to EVERY repository, without exception** — ⚠️ including one where a single
person writes. ⛔ **A proposal that one person opens and reviews alone still leaves the change
readable before it enters, which is what it is for.**

---

## 3 · THE LOOP — every change, no exceptions

```
PRE-FLIGHT → BRANCH → IMPLEMENT → VERIFY → COMMIT → UPDATE CONTEXT → PROPOSE → ⛔ STOP
                                                                                  │
                    ⬇ and AFTER the stop — a human decision — the cycle continues ⬇
                                                                                  │
                    CONFLICT? → MERGE (human) → DETECT → VERIFY IT TRAVELLED → DELETE
```

> ## ⭐ THE CYCLE DOES NOT END AT THE STOP.
> ⚠️ **Measured: a declared cycle that ended at "propose" left everything after it off every
> map** — ⛔ **and a gap nobody names is indistinguishable from one that does not exist.**

### ⭐ THE TWELVE STAGES — each one with the rule that governs it

| # | Stage | ⭐ Governed by |
|---|---|---|
| 1 | **PRE-FLIGHT** — read before touching | §4 |
| 2 | **BRANCH** — ⛔ never on the base | §4 · a gate |
| 3 | **IMPLEMENT** — only what the scope allows | ⭐ `rule-working-in-a-block.md` §4 |
| 4 | **VERIFY** — ⛔ every check, no excuses | ⭐ the validation owner |
| 5 | **COMMIT** — atomic, with its reason | §4 |
| 6 | **PROPOSE** — ⭐ with its link handed over | §5 |
| 7 | ⭐ **GROUP** — a ceiling per proposal; the last one closes the block | §6 |
| 8 | **CONFLICT** — ⭐ diagnose before resolving | §7 |
| 9 | 🔴 **MERGE** — ⛔ **a human decision, never the agent's** | §5 |
| 10 | ⭐ **DETECT the merge** — look, do not ask | §8 |
| 11 | ⭐ **VERIFY IT TRAVELLED** — before deleting anything | §8 |
| 12 | **DELETE the branch** — local and remote, ⚠️ with its exceptions | §8 |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-CYC-001` | ⭐ **No stage is without an owner** | 🔒 | ⛔ an unowned stage is one nobody performs |
| `SHP-CYC-002` | 🔴 **The agent stops at the proposal** | 📖 | ⭐ merging is a human decision |

---

## 4 · THE STAGES BEFORE THE PROPOSAL

### Pre-flight — ⛔ before writing any code

⭐ Read the project's entry point · the specification the work references · ⚠️ **what just shipped
and what broke** · the known issues, ⭐ **so a past mistake is not repeated** · the conventions of
whatever is being touched.

> ⭐ **And here a gate beats a habit.** ⚠️ **A person can forget to read; a gate that injects the
> standard before the edit cannot.**

### Branch · Implement · Verify · Commit

| Stage | ⭐ The rule |
|---|---|
| **branch** | ⭐ one branch per unit of work, ⛔ **never the base** |
| **implement** | only files in scope · ⭐ follow the patterns around you · ⛔ **if the spec is unclear, flag it — never guess** |
| **verify** | ⭐ **which checks apply depends on the discipline**, and the block declares it |
| **commit** | atomic, ⭐ with the reason in the body — ⛔ not only the what |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-VER-001` | ⛔ **A failing check is fixed before proceeding** | 🟡 | ⭐ never commit broken work |
| `SHP-VER-002` | ⭐ **"It probably works" is not a verification** | 📖 | ⚠️ see the validation criterion |
| `SHP-CTX-001` | ⭐ **The context record is updated BEFORE proposing** | 🟡 | ⛔ what shipped, what broke, what was learned |

---

## 5 · THE PROPOSAL

### ⭐ What its body must carry

**What** it does · **why** · ⭐ **the reference it implements** · what changed · ⚠️ **notes for the
reviewer** — trade-offs, open questions, follow-ups — and the verification list:

```
[ ] ⛔ the base is correct           [ ] no secret committed
[ ] every discipline check passes    [ ] only in-scope files modified
[ ] the context record is updated
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-PRP-001` | ⭐ **The proposal's link is handed over, every time** | 📖 | ⛔ see below |
| `SHP-PRP-002` | 🔴 **The agent does not merge** | 📖 | ⭐ creating it is the end of its job |

> ## ⭐ A PROPOSAL THAT CANNOT BE OPENED IN ONE CLICK IS NOT DELIVERED.
> ⚠️ It goes in the delivery block, ⭐ **and it is repeated on every update** — a link given once,
> three messages ago, is a link the reader has to go find.

---

## 6 · ⭐ GROUPING — how much goes in one proposal

⬜ **Declare the ceiling for this installation.** ⭐ **What the engine fixes is that there IS one**,
not what it is:

```
items_per_proposal: 4
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-GRP-001` | ⭐ **A ceiling is declared, never inferred** | 🔒 | ⛔ undeclared means each reader assumes one |
| `SHP-GRP-002` | ⭐ **The LAST proposal of a block is its CLOSURE — ⛔ it does not wait to fill the group** | 📖 | ⚠️ see below |

⭐ **`SHP-GRP-002` is the exception that keeps the rule usable.** ⛔ **A block held open waiting for
a fourth item is a block whose state goes stale while nothing happens** — and the ceiling exists
to reduce review cost, ⚠️ **not to delay closure.**

⚠️ **Why group at all:** ⭐ reviewing one change costs almost as much as reviewing four related
ones, ⛔ **and four unrelated ones cost more than four separate reviews.** The ceiling is a
grouping rule, not a batching quota.

---

## 7 · ⭐ A PROPOSAL WITH CONFLICTS — diagnose before resolving

> ## ⭐ ALMOST ALWAYS IT IS THE HISTORY REWRITE, NOT RIVAL WORK.

| # | Step | ⚠️ |
|---|---|---|
| 1 | ⭐ **DIAGNOSE** — is this real divergence, or a rewritten history? | ⛔ **and this is the step that gets skipped** |
| 2 | **Bring the base in** — rebase onto the current base | |
| 3 | **Push with a lease**, never a bare force | ⭐ a lease refuses if somebody else moved |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-CNF-001` | ⭐ **Diagnose before resolving** | 📖 | ⛔ nothing verifies this |
| `SHP-CNF-002` | 🔴 **A GENERATED file is never resolved — it is REGENERATED** | 📖 | ⭐ see below |
| `SHP-CNF-003` | ⛔ **Never a bare force push on a shared branch** | 📖 | ⚠️ it discards what you cannot see |

> ## ⭐ `SHP-CNF-002` — resolving a generated file by hand is choosing a lie
> ⛔ **Both sides of the conflict are outputs, and the correct content is neither: it is whatever
> the generator produces from the merged input.** ⚠️ **Picking one side commits a state that never
> existed.**

---

## 8 · ⛔ AFTER THE MERGE — verify, THEN delete

```
1 · VERIFY   the change is in the base · the diff against the base is empty
2 · DELETE   the branch, local and remote
```

> ## ⛔ DELETING BEFORE VERIFYING DESTROYS THE ONLY COPY OF WHAT THE MERGE LEFT OUT.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-DEL-001` | ⭐ **Verify it travelled, then delete** | 🟡 | ⛔ never the reverse |
| `SHP-DEL-002` | ⭐ **Use the refusing delete, never the forcing one** | 📖 | ⚠️ see below |
| `SHP-DEL-003` | ⭐ **A branch is deleted, not kept "just in case"** | 📖 | ⛔ two exceptions, below |
| `SHP-DEL-004` | 🔴 **Never commit onto a branch whose proposal already merged** | 📖 | ⭐ see below |

### ⭐ THE REFUSING DELETE IS THE LAST LOCK

⚠️ **The lowercase delete REFUSES when the branch holds commits the base does not; the uppercase
one deletes in silence.** ⭐ **That refusal is the last lock before losing work.**

⛔ **And a history rewrite makes it complain even when everything did travel** — ⚠️ so its
complaint forces you to **look at the content.** ⭐ **Never to force past it without looking.**

### 🔴 THE MEASURED INCIDENT — why this is a rule and not advice

⚠️ **Two proposals merged nine seconds apart. Both showed as merged.** ⛔ **The second one's work
never reached the base: nine files, hundreds of lines, with the merged label on.**

> ## ⭐ THE MECHANISM, so nobody has to rediscover it
> ⚠️ **A squash flattens a branch's commits into a NEW commit on the base.** ⛔ **That commit is
> not a descendant of the original branch, so the parentage breaks at the moment of the merge.**
>
> ⭐ **A proposal chained onto that branch then merges against an ancestor that no longer is one,
> and its work is left dangling** — ⛔ **no conflict, no warning, nothing visible.**
>
> ## ⛔ THE MERGED LABEL DOES NOT MEAN THE CODE IS IN THE BASE.

### ⭐ THE TWO EXCEPTIONS — the branch is kept

| Case | ⭐ Why |
|---|---|
| **a major version migration** | ⭐ the branch is the only intact state of the "before"; a rollback needs it whole |
| ⭐ **irreversible, in production, or touching real data** | ⚠️ **the test is *"what if we have to go back TODAY?"*, not the size of the change** |

⛔ **Outside those two: it gets deleted.** ⚠️ **Doubt does not keep a branch — it asks.** ⭐ Keeping
things "just in case" is how a workspace ends up with ten dead branches.

### 🔴 A BRANCH WHOSE PROPOSAL ALREADY MERGED IS DEAD

⭐ **Measured: the working copy said "ahead by one" and it was true AND misleading at once** —
⚠️ ahead of *that branch's* remote, ⛔ **not of the base.**

> ## ⛔ THE LOCAL BRANCH DOES NOT KNOW ITS PROPOSAL WAS MERGED.
> ⭐ **A proposal opened from there proposes the wrong base.** The fix: a **new branch from the
> current base**, and carry the commits over — ⛔ never more commits on top.

---

## 9 · 🔴 THE BASE — what a change is proposed against

> ## ⛔ THE BASE IS THE MAIN LINE. NEVER ANOTHER BRANCH.

⚠️ **Chaining is only safe where merges keep both parents.** ⭐ **Where history is squashed,
chaining loses work silently** — §8 is the measurement.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-BAS-001` | ⭐ **The base is checked before opening anything** | 🔒 | ⛔ a wrong base is not recoverable after the merge |
| `SHP-BAS-002` | ⭐ **A real dependency is resolved by WAITING, never by chaining** | 📖 | ⚠️ bring the base in and rebase |
| `SHP-BAS-003` | **Open proposals are audited for chaining** | 🔒 | ⭐ detection, not only prevention |

### ⭐ WHY THIS IS A SCRIPT AND NOT A PARAGRAPH

⚠️ **The written rule already existed. A recorded memory of the same failure already existed, from
having hit it twice in one day.** ⭐ **Both were read at the start of the session — and neither was
applied when the base was chosen.**

> ## ⛔ HAVING THE FACT DID NOT PREVENT THE ERROR.
> ⭐ **The written rule scored 0 out of 1 on the day it mattered.** ⚠️ **That is why there is a
> check, and why the battery verifies the check is still in place.**

⭐ **And detection matters as much as prevention:** ⛔ the post-mortem detector **did** catch this
incident — ⚠️ **after the merge**, which is the wrong side of it.

---

## 10 · 🔴 THE ANTI-PATTERNS — never, in any change, in any discipline

| # | ⛔ Anti-pattern | ⭐ Why |
|---|---|---|
| 1 | **pushing straight to the base** | §2 — measured at 0 of 15 |
| 2 | ⭐ **skipping the full verification** because one check passed | ⚠️ one green is not the suite |
| 3 | **touching files outside the scope** | ⛔ the block's boundary |
| 4 | ⭐ **guessing when the spec is unclear** | ⛔ ask or flag — ⚠️ never invent |
| 5 | **leaving the context record un-updated** | ⭐ §11 |
| 6 | ⛔ **force-pushing a shared branch** | ⚠️ it discards what you cannot see |
| 7 | 🔴 **committing a secret, a key, or a configuration file that holds one** | ⭐ what is written stays in history |
| 8 | 🔴 **a proposal that depends on another un-merged one** | ⛔ §9 — ⚠️ **and the usual "unless explicitly stacked" exception does NOT apply where history is squashed** |

⭐ **Anti-pattern 8 carries its own exception being revoked**, and that is deliberate: ⚠️ **the
general advice is safe only under a condition most workspaces do not meet.**

---

## 11 · ⛔ CLOSING THE SESSION — the cut that saves nothing

> ## ⭐ A CONTEXT RESET IS A CUT, NOT A SAVE. It writes nothing.

⛔ **Whatever is not on disk is lost, with no warning.**

| # | ⭐ What gets written, in this order |
|---|---|
| 1 | 🔴 **the session record** — what happened, and what it cost |
| 2 | ⭐ **the cold-start brief** — where we stopped and what is next |
| 3 | the period's milestones |
| 4 | ⭐ one memory per fact, with its index line |
| 5 | the findings that are not urgent |
| 6 | ⭐ **the active block** — its state, its decisions, its context consolidated |

### ⬜ WHERE EACH ONE LIVES

⛔ **The rule demanded six artifacts and named the location of none**, so nothing could check that
any of them existed. A lock over an artifact with no declared address is not a lock.

| # | ⬜ Path | Ships as |
|---|---|---|
| 1 | ⬜ session record | ⬜ declare it — the engine ships no default |
| 2 | ⬜ cold-start brief | `templates/RETOMAR.md.template` → the instance names where it lands |
| 6 | ⬜ the active block | ⭐ resolved from the block itself, never declared here |

⭐ **The engine fixes that there IS a place, never which one.** ⛔ A path missing from this table
is ⬜ NOT MEASURED, and the check says so rather than passing in silence.

⚠️ **These are INSTANCE files.** They are born from a template at install time, so an
un-instantiated engine legitimately has none — ⛔ **and a check that demanded them would report
every fresh clone as broken.** What is verified is that the path is DECLARED, and that a declared
one resolves.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SHP-CLS-001` | 🔴 **No context reset before the session is recorded** | 🔒 | `bin/check-shipping` · against the ⬜ paths above |
| `SHP-CLS-002` | ⭐ **The record states what the session COST, not only what it did** | 🟡 | ⚠️ size, duration, peak context |
| `SHP-CLS-003` | ⭐ **The cold-start brief is refreshed, not appended to** | 📖 | ⛔ a brief that grows stops being read |

### 🔴 THE MEASUREMENT — why this needs a lock

⚠️ **Of the sessions in one project, fewer than half had ever been recorded.** ⛔ **The worst was
also the largest: days open, an enormous context, and invisible in every record.**

> ## ⭐ AND FROM THAT UNRECORDED SESSION CAME THE WORST INCIDENT IN THE PROJECT.
> ⚠️ **It was documented nowhere.** ⛔ **It had to be recovered from raw logs, days later** — and
> only because somebody went looking.

⭐ **That is what an unrecorded session costs: not the session, but the ability to explain what
happened in it.**

---

## 12 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **committing on the base** | ⛔ the change enters unreviewed, ⭐ and the habit is measured at 0 of 15 |
| ⭐ **the wrong base** | ⛔ **the work is lost with the merged label on** |
| **deleting before verifying** | ⭐ the only copy of what the merge left out |
| ⭐ **forcing past the refusing delete** | ⚠️ the last lock, removed by hand |
| **committing on a merged branch** | ⭐ every proposal from there has the wrong base |
| ⭐ **resolving a generated file** | ⛔ **a state that never existed, committed** |
| **the link not handed over** | ⚠️ the reader goes looking, ⭐ and often does not |
| ⭐ **a reset with no record** | ⛔ **the session is invisible, and so is whatever went wrong in it** |
| **the brief left stale** | ⭐ the next session starts by inferring, confidently and wrongly |

---

## 13 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the grouping ceiling, the branch names, the base's name | ⭐ the owner — ⚠️ **declared once** |
| the loop, the twelve stages, the anti-patterns | whoever maintains the engine, through a recorded decision |
| ⛔ deleting a branch before verifying | **nobody** — ⭐ ⚠️ **it is not reversible** |
| ⛔ merging on the agent's own decision | **nobody** — ⭐ that is the human's line |

---

Related: `README.md` (⭐ the three document types) · `contract-block.md` (⭐ **§K — the last
proposal of a block is its closure**) · `rule-working-in-a-block.md` (⭐ §3 the lane that decides
how much process, §6 the friction this file will produce) · `contract-document.md` ·
`../memory/principles/owner-3-validation.md` (⭐ what "verified" means at stage 4) ·
`../bin/check-shipping` (what enforces the 🔒 rows).
