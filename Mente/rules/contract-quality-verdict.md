# CONTRACT · QUALITY VERDICT

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** the verdict a block carries when it closes
**Enforcement:** 🔒 partial — `bin/grade-block` is layer 1; layer 2 is criterion
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/grade-block` · `bin/probes/probe-grade.py`

## Purpose

Answers one question a linter cannot: **is this a product, or an MVP?** ⛔ Not *"does it run"* —
whether it is finished to a standard somebody would defend.

### 🔴 THE FAILURE THAT MADE THIS NECESSARY

⚠️ **Measured, and reproducible:**

```
21:15   "the system is complete"
06:33   "what is wrong is that this file implements it halfway"
```

⭐ **The same code. Opposite verdicts. Nine minutes apart.** The only thing that happened in
between was a context reset.

> ## ⛔ A VERDICT THAT CHANGES WITH CONTEXT IS NOT A VERDICT — IT IS A MOOD.
> ⚠️ **And the direction it drifts is always the same:** with the work fresh it reads finished;
> read cold, the same files read halfway. Neither reading is dishonest, and that is the problem.

> ## 🚫 THE AGENT DOES NOT DECLARE "THIS IS FINE." IT REPORTS THE MEASUREMENT.

---

## 1 · ⭐ TWO LAYERS, AND THEY ARE NOT INTERCHANGEABLE

| Layer | What it answers | Who supplies it | Reproducible |
|---|---|---|---|
| **1 · measured** | the numbers: dead files, duplication, cycles, secrets, missing rollbacks | ⭐ **nobody — a script measures it** | 🟢 identical on every run |
| **2 · criterion** | *is that piece with five dependents well cut, or badly cut?* | ⬜ **the installation's owner** | ⚠️ requires judgment |

⛔ **Layer 1 without layer 2 is a linter.** ⛔ **Layer 2 without layer 1 is an opinion.**
⭐ **The verdict is the pair.**

> ## ⭐ ANY LINTER HAS LAYER 1. WHAT NO LINTER HAS IS A SENIOR'S CRITERION.
> ⛔ **And that criterion belongs to whoever owns the installation, never to the agent** — an
> agent that writes its own quality dimensions has written a linter and called it a review.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `QLT-LAY-001` | 🔴 **Layer 1 is measured by a script, never asserted** | 🔒 | `bin/grade-block` |
| `QLT-LAY-002` | ⭐ **Layer 2 criterion is declared by the installation, never by the agent** | 📖 | ⬜ each dimension carries a declared criterion or stays `⬜` |
| `QLT-LAY-003` | **A closing verdict names BOTH layers** | 🔒 | `bin/grade-block` prints layer 2's state beside layer 1's · ⭐ and the RECORD keys them apart |

> ## ⭐ `QLT-LAY-003` · THE ONE WHO MEASURES IS NOT THE ONE WHO DECIDES
> ⛔ **Whoever produces the evidence must not decide what it proves.** Layer 1 answers *"this is
> what I observed"*; layer 2 answers *"with this, it closes or it does not"*. ⚠️ Merged, an agent
> satisfies the bar by choosing what to measure — and the bar was the only thing stopping it from
> declaring itself done.
>
> ⚠️ **The printed report kept them apart and the RECORD did not.** `close.json` carried a key
> called `verdict`, and a machine re-reading it has no way to know that is layer 1 alone — ⛔ with
> every dimension still ⬜ undeclared, that number cannot be a closing verdict at all.
>
> | Key | Says |
> |---|---|
> | `layer1_verdict` | ⭐ what was MEASURED — a script's answer, never an opinion |
> | `dimensions` | ⬜ which of the six layer-2 criteria are still undeclared |
> | ⛔ `verdict` | **nothing writes this.** The closing authority is a person, and a person does not sign through a field a script filled in |

---

## 2 · 🔴 THE TYPE DECIDES THE RULER

⛔ **Measuring the wrong metric produces a false red, and a false red teaches people to ignore
reds.** A documentation block has no test file to be missing; an infrastructure block has no
import graph.

| Type | What is measured | What does not apply |
|---|---|---|
| `code` | dead files · unused exports · duplication · cycles · test files · declared dependents | — |
| `docs` | broken links · orphan documents | ⬜ tests, imports, duplication |
| `infra` | a documented runbook · a documented rollback | ⬜ tests, imports, duplication |
| `data` | migrations · ⭐ migrations **without** a rollback | ⬜ tests, duplication |
| **every type** | 🔴 **secret values written down** | ⛔ never n/a |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `QLT-TYP-001` | 🔴 **A block declares its type, or it cannot be graded** | 🔒 | `bin/grade-block` refuses |
| `QLT-TYP-002` | ⭐ **A metric that does not apply is `⬜`, never a pass** | 🔒 | ⛔ n/a and green must never render alike |
| `QLT-TYP-003` | 🔴 **A pasted secret is red for EVERY type** | 🔒 | there is no block kind where it is acceptable |

### ⛔ `⬜` IS NOT A GREEN, AND THE DIFFERENCE IS THE WHOLE POINT

⚠️ **A metric that does not apply and a metric that passed produce the same silence** unless the
report distinguishes them. ⭐ **Not measured is NOT a pass** — the report prints `⬜` with the
reason it does not apply, so a reader can tell "checked, clean" from "never looked".

---

## 3 · 🔴 ABSENCE OF EVIDENCE IS NOT EVIDENCE

⛔ **Measured:** a block whose declared scope resolved to **nothing** had zero broken links and
zero orphan documents — and scored 🟢 **PRODUCT**.

### ⚠️ AND HALF A SCOPE IS THE HARDER CASE

⛔ **Measured on a real block: three paths declared, one resolved, verdict 🟢 PRODUCT.** Two
thirds of what the block claims to own was never looked at — ⭐ **and every number in the report
was correct.**

> ## ⛔ ZERO FILES IS CAUGHT BY THE COUNT. HALF A SCOPE IS NOT.
> ⚠️ **The count was not zero, so the rule above stayed silent** — and a partial measurement
> reported as a full one is the shape nobody thinks to check.

> ## ⭐ A VERDICT OVER ZERO MEASURED FILES IS NOT A PASS. IT IS `NOTHING MEASURED`.
> ⚠️ **This is the emptiest kind of green, and the hardest to notice**, because every number in
> the report is genuinely correct.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `QLT-EVD-001` | 🔴 **Zero measured files is `NOTHING MEASURED`, never a pass** | 🔒 | `bin/grade-block` |
| `QLT-EVD-002` | **The report names the scope it measured** | 🔒 | ⛔ a verdict whose scope is unstated cannot be reproduced |
| `QLT-EVD-003` | 🔴 **A scope that resolves PARTLY is not a scope that resolved** | 🔒 | `bin/grade-block` · ⛔ measured: 3 paths declared, 1 resolved, verdict 🟢 |

---

### ⛔ EVERY METRIC IS MEASURED INSIDE THE BLOCK'S SCOPE — NEVER THE WHOLE REPOSITORY

⭐ **Measured, comparing two implementations of this same layer on one real block:** counting test
files across the whole repository reported **152**; counting them inside the block's declared
scope reported **4**.

> ## ⛔ A BLOCK WITH NO TESTS PASSES THE TEST ROW BECAUSE A DIFFERENT BLOCK HAS 152.
> ⚠️ **The number is real and the row is green, and neither says anything about this block.**

⭐ **The scope is what the block declared it owns.** A metric measured outside it grades somebody
else's work — and grades it *favourably*, which is the direction nobody checks.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `QLT-SCP-001` | 🔴 **Every metric is measured inside the declared scope** | 🔒 | `bin/grade-block` |
| `QLT-SCP-002` | ⭐ **A metric that reaches outside the scope is a false green** | 🔒 | ⛔ it borrows another block's evidence |

---

## 4 · THE VERDICT — three states, and MVP is not a shrug

| Verdict | When | What it permits |
|---|---|---|
| 🟢 **PRODUCT** | no red, no yellow | closes as a product |
| 🟡 **CLOSE** | yellows, no red | closes, with its concerns listed |
| 🔴 **MVP** | any red | ⭐ **closes — marked MVP, with its debt listed** |
| ⬜ **NOTHING MEASURED** | nothing in scope | ⛔ does not close: fix the scope |

> ## ⭐ A 🔴 DOES NOT FORBID CLOSING THE BLOCK. IT FORBIDS CLOSING IT **AS A PRODUCT**.
> ⚠️ **This is deliberate.** A verdict that blocks work gets bypassed; one that labels it gets
> used. ⛔ What is forbidden is closing an MVP *while calling it a product* — the label is the
> enforcement, not the gate.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `QLT-VRD-001` | ⭐ **An MVP closes with its debt LISTED, never with it hidden** | 🔒 | `bin/grade-block` names the rows that must appear in the closing |
| `QLT-VRD-002` | **The verdict is reproducible: same code, same verdict** | 🔒 | ⛔ that is the failure this contract exists for |

---

## 5 · ⬜ THE SIX DIMENSIONS OF LAYER 2

⭐ **The frame travels with the engine. The criterion does not.** Each dimension carries three
parts, and the third is what makes it usable:

| Part | Purpose |
|---|---|
| **Question** | what is judged, in one concrete sentence |
| 🔴 **Required evidence** | ⭐ **what must be SHOWN** — asserting is not answering |
| **Typical failure** | what it looks like when wrong, from a real case |

> ## ⛔ A LOOSE CRITERION IS USELESS.
> ⚠️ *"The architecture must be correct"* is as empty as *"it is fine"*. **That is why every
> dimension demands evidence, and why an answer without it does not count.**

| # | Dimension | The question | Required evidence |
|---|---|---|---|
| **1** | architecture | does each piece do one thing, in the right layer? | the dependency tree + which piece would break how many others |
| **2** | data design | does the schema represent the domain — are impossible states impossible? | the real schema + one case it **cannot** represent wrongly |
| **3** | abstraction | ⭐ neither copied three times **nor** generalized for a single caller | where it repeats, **or** the real callers of the abstraction |
| **4** | naming | does the name say what it does, without reading the body? | explain three names ⛔ **without opening the file** |
| **5** | contracts | are the interfaces declared — are errors part of the contract? | the real signature + what happens when it fails |
| **6** | 🔴 necessity | does **every file that exists have to exist?** | for each file: who consumes it, and why it could not live elsewhere |

**Verdict per dimension:** 🟢 pass · 🟡 concern, documented, does not block · 🔴 fail.

### ⬜ DECLARE YOUR CRITERION

⬜ **One block per dimension: what makes it pass HERE.** ⛔ A dimension with no declared criterion
is permanently `⬜` — which is honest, and does not pretend to be a review.

⭐ **Written so two people reach the same verdict from the same evidence.** ⛔ Until a row is
filled, the dimension reports as `⬜ undeclared` — and `grade-block` counts the empty rows, so the
number in its report is measured, never asserted.

| # | Dimension | ⬜ What makes it pass HERE |
|---|---|---|
| 1 | architecture | ⬜ undeclared |
| 2 | data design | ⬜ undeclared |
| 3 | abstraction | ⬜ undeclared |
| 4 | naming | ⬜ undeclared |
| 5 | contracts | ⬜ undeclared |
| 6 | necessity | ⬜ undeclared |

⚠️ **Replace `⬜ undeclared` with the criterion, never delete the row** — a deleted row is a
dimension nobody will notice is missing.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `QLT-DIM-001` | 🔴 **A dimension is answered with EVIDENCE, never with an assertion** | 📖 | ⛔ "looks fine" is not an answer |
| `QLT-DIM-002` | ⭐ **A dimension with no declared criterion stays `⬜`** | 🔒 | `bin/grade-block` counts them and says how many |
| `QLT-DIM-003` | ⚠️ **Dimension 3 evaluates BOTH sides** | 📖 | ⛔ hunting duplication alone passes the abstraction built for one caller |

### ⚠️ WHY DIMENSION 3 CUTS BOTH WAYS

⛔ **Copied too many times and generalized too early are the same failure from opposite ends.** A
review that only hunts duplication waves through an abstraction with a single caller — ⭐ and that
one is *harder* to remove later, because it looks deliberate.

⭐ **There is no fixed repetition count that forces an abstraction.** Three copies of two trivial
lines may be fine; two copies of one rule are not. **What decides is whether the copies have to
change together.**

---

## 6 · ⭐ WHAT LAYER 1 CANNOT SEE

⚠️ Kept explicit so nobody mistakes a green layer 1 for a finished review.

| Layer 1 measures | ⛔ It cannot judge |
|---|---|
| a file nobody imports | whether a file **with** importers should exist at all |
| a piece with many dependents | whether those dependents mean it is **well** cut or **badly** cut |
| a duplicated block | whether the copies **have to change together** |
| a name exists | whether the name **says what it does** |
| a function has no error path | whether the error is **part of the contract** |

> ## ⭐ LAYER 1 FINDS WHAT IS WRONG. LAYER 2 DECIDES WHETHER IT MATTERS.
> ⛔ **A block that is green on layer 1 and never saw layer 2 has been linted, not reviewed** —
> and the difference is invisible in the report unless it says so.

---

## 7 · ⬜ WHAT EACH INSTALLATION DECLARES

⛔ **These are not the engine's to fix.** A threshold chosen elsewhere measures somebody else's
project.

| ⬜ Declaration | Default | Why it is not the engine's |
|---|---|---|
| ⬜ code file extensions | `.py .js .ts .tsx .jsx` | ⛔ a project in another language measures nothing, silently |
| ⬜ duplication window | 8 lines | shorter finds noise, longer finds nothing |
| ⬜ duplication tolerance | more than 2 blocks is red | ⚠️ a generated-code tree lives above it legitimately |
| ⬜ excluded directories | build output, dependencies, VCS | every ecosystem names these differently |

⭐ **Declared where the installation can see them, never buried in the script** — ⛔ a threshold
that lives only in code is a decision nobody knows was taken.

---

## 8 · THE OUTPUT

```
BLOCK <name> · type: code — measured quality · <date>
  scope: <the directories measured>

  secret values written down ............    0  🟢
  files nobody imports (dead code) ......    1  🔴
  exports never imported ................    3  🟡
  duplicated blocks (>=8 lines) .........    0  🟢
  test files ............................    7  🟢
  import cycles .........................    0  🟢
  --------------------------------------------------------
  LAYER 1 VERDICT: 🔴 MVP   (metrics for type `code`)

  ⬜ = not measured for this type. It is NOT a pass.
  Layer 2 (criterion) is rules/contract-quality-verdict.md §5.
  A 🔴 does not forbid closing the block. It forbids closing it AS A PRODUCT.
```

---

**Decided by:** `decisions/ADR-028-the-type-changes-the-ruler.md` — ⭐ **why the type changes the RULER and never the BAR**, and why `n/a` is never green.
**Also decided by:** `decisions/ADR-014-the-criterion-belongs-to-the-owner.md` — ⭐ **whose criterion layer 2 is**, and why an agent writing its own dimensions has written a linter.
**Also decided by:** `decisions/ADR-013-the-verdict-has-two-layers.md` — ⭐ **why two layers**, what each one fails at alone, and the nine minutes that produced the decision.

## WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ which dimensions this installation weighs | ⭐ the owner — ⚠️ **declared before the verdict, never after seeing it** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ raising a 🔴 MVP to 🟢 PRODUCT without new evidence | **nobody** — ⭐ the verdict follows the measurement, never the other way |
| ⛔ grading your own work as the deciding voice | **nobody** — ⚠️ whoever produces the evidence is not who decides what it authorises |

⚠️ **The bar is declared before the work is measured against it.** ⛔ A standard chosen after
seeing the result converges on *"whatever this already does"*, which is the circular authority
this file exists to break.

---

Related: `rules/contract-block.md` (the closing that carries this verdict) ·
`rules/rule-checks-must-measure.md` (why layer 1 must be able to fail) ·
`rules/rule-config-hygiene.md` (the pasted-secret rule this enforces per block) ·
`../memory/principles/owner-3-validation.md` (the figure that applies layer 2 at close).
