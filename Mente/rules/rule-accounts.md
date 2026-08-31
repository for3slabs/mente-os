# RULE · ACCOUNTS

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** ⭐ **every repository this installation pushes to** — whatever it contains
**Enforcement:** 🔒 partial — `bin/check-accounts` + two gates · ⚠️ **some rows here are 📖**
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-accounts` · `bin/probes/probe-accounts.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone
**Size:** a BASE file — it ships whole. See `contract-document.md` §4.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ Which account governs which repository, and how work is stopped from leaving to the wrong one.

⚠️ **The failure it prevents is not losing work. It is work that arrives somewhere nobody looks
again** — a retired repository, an account that is not yours, an address that still resolves
because the host kept redirecting it.

⛔ **And every one of those pushes SUCCEEDS.** There is no error to notice. The work is gone in the
only way that leaves no trace: it went somewhere, and it was the wrong somewhere.

---

## 1 · ⭐ THE REGISTRY IS THE DECLARATION, AND A SCRIPT CHECKS IT

`cuentas.tsv` names every repository this installation may push to. ⬜ It is **instance data** —
a clone receives the header and zero rows, because nobody inherits somebody else's accounts.

> ## ⚠️ WHY A FILE AND NOT MEMORY
> ⭐ **"Which account governs this repo" is a fact that lives in three places at once** — the
> remote, the documentation, and somebody's memory — ⛔ **and nothing compares them.** They drift,
> and the drift is silent.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ACC-REG-001` | ⭐ **A push target is declared before it receives work** | 🔒 | ⛔ an undeclared destination aborts the push |
| `ACC-REG-002` | ⭐ **Every row justifies why that repository exists** | 🔒 | ⚠️ one that cannot is duplicated or abandoned work |
| `ACC-REG-003` | ⛔ **No credential in the registry — the `guia` column POINTS** | 🔒 | ⚠️ ⭐ what is written stays in history |
| `ACC-REG-004` | ⭐ **A role used is a role declared** | 🔒 | ⛔ an undeclared role passes silently |

⭐ **`ACC-REG-004` is not bookkeeping.** A validator can only check the roles it knows. ⛔ **A role
invented in a row and never declared is one nothing measures** — and that is exactly how a retired
repository keeps receiving work.

---

## 2 · 🔴 A RETIRED REPOSITORY RECEIVES NO WORK

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ACC-ARC-001` | 🔴 **A repository whose role is `archivado` refuses a push** | 🔒 | ⭐ checked BEFORE "is it registered" |

⭐ **The order matters, and it is the whole rule.** ⛔ **An archived repository IS registered** — it
stays in the table on purpose, because one that disappears from the table becomes invisible again
and the reason it was retired disappears with it.

⚠️ **So a gate that asks "is this registered?" first answers YES and lets the push through.**
Measured: two layers both authorised pushing to a repository that had been retired that same
morning. The role was stored, and no piece read it.

> ## ⭐ A FIELD NOBODY READS IS NOT A RULE. It is a comment with a column.

---

## 3 · ⛔ TWO LAYERS, BECAUSE ONE OF THEM CAN BE WALKED AROUND

| Layer | What it is | Reach |
|---|---|---|
| **1 · the warning** | reads the COMMAND, explains before anything happens | ⚠️ can be walked around |
| **2 · the abort** | runs inside the push itself, destination already resolved | ⭐ **cannot be walked around** |

> ## 🔴 THE MEASUREMENT THAT FORCED LAYER 2
> A gate that reads the text of a command was tested with seven ways of writing the same push.
> ⛔ **Five got through**: an alias, a shell function, a variable holding the verb, an `eval`, and
> an argument-builder. The recorded debt said "an alias"; the reality was five.

⛔ **The lesson generalises beyond pushing:** ⭐ **a pattern over command text NEVER covers every
way of invoking a command.** ⚠️ It does not matter how many patterns are added — there is always
one more. **A defence that lives only there is a defence with a schedule.**

⭐ **Layer 2 has no text to interpret.** It runs when the operation is already happening, with the
destination resolved by the tool itself. However the command was written, it arrives here.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ACC-LYR-001` | ⭐ **The unavoidable layer exists, not only the readable one** | 🔒 | ⛔ a text pattern is not a lock |
| `ACC-LYR-002` | ⭐ **Layer 1 explains; layer 2 decides** | 📖 | ⚠️ ⛔ a warning nobody can act on is noise |
| `ACC-LYR-003` | 🔴 **Layer 2 fails CLOSED** | 🔒 | ⛔ there is no "ask" inside a push |
| `ACC-LYR-004` | 🔴 **Layer 2 is WIRED, not merely present** | 🔒 | ⛔ an unlinked hook never runs, and looks installed |

> ## 🔴 `ACC-LYR-004` IS THE ONE THAT LOOKS FINE AND IS NOT
> ⭐ **A hook file that exists but is not linked into the tool's hook directory NEVER RUNS.** ⛔ The
> file is there, the code is correct, the probe passes — and the layer that cannot be walked around
> is not running at all. ⚠️ **Nothing distinguishes that from a working installation except
> looking**, which is why a script looks.

⚠️ **`ACC-LYR-003` needs its reason said out loud.** ⭐ **Aborting costs nothing** — the work stays
local, and nothing is lost. ⛔ **Letting an unverified destination through costs everything**, and
the cost is invisible: the push succeeds.

---

## 4 · ⚠️ MORE THAN ONE REMOTE IS A DIVERGENCE WAITING

⭐ **When a clone declares several remotes, pushing to one leaves the others behind.** ⚠️ Nothing
reports it, because each push individually succeeded.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ACC-MUL-001` | ⚠️ **A push names the remotes it is NOT updating** | 🔒 | ⭐ a warning, never a block |

⛔ **Deliberately a warning.** Pushing to one remote at a time is legitimate and common; blocking
it would make an ordinary operation impossible. ⭐ **What is not legitimate is not KNOWING** — the
divergence is silent, and silence is what makes it last.

---

## 5 · ⚠️ A ROW IS A CLAIM UNTIL IT IS MEASURED

> ## 🔴 THE TRAP THAT LOOKS LIKE SUCCESS
> ⭐ **A renamed or transferred repository usually keeps redirecting from its old address.** ⛔ Both
> names resolve, both look alive, and a stale row points at a dead repository while everything
> appears to work.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ACC-VRF-001` | ⭐ **A declared local path is checked against the machine** | 🔒 | ⛔ a path that does not exist was never verified |
| `ACC-VRF-002` | ⚠️ **A row with no local path is a claim, and says so** | 🔒 | ⬜ NOT MEASURED, never a pass |

⭐ **`ACC-VRF-002` is why the validator reports rather than stays quiet.** ⛔ A row nothing can
check is not evidence of anything, and reporting it as fine is the failure this system names
first: **absence of evidence read as evidence of absence.**

---

## 6 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **an undeclared destination** | ⛔ work arrives where nobody looks, and the push succeeded |
| ⭐ **a retired repository still receiving** | ⚠️ **the work is in a place already declared dead** |
| **only the readable layer** | ⛔ five ways of writing the same command walk past it |
| **no `por_que_existe`** | ⚠️ nobody can tell duplicated work from a second copy on purpose |
| ⭐ **a credential in the registry** | 🔴 **it is rotated, not deleted** — the file is in history |

---

Related: `rule-shipping.md` (how a change leaves the workspace) · `rule-config-hygiene.md`
(⛔ the secret rules this one inherits) · `../templates/cuentas.tsv.template` (the registry's
shape) · `../secrets/README.md` (where the `guia` column points) · `contract-document.md`.
