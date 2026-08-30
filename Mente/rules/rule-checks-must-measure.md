# RULE · CHECKS MUST MEASURE

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every validator, gate and hook in this system
**Enforcement:** 🔒 partial — `bin/check-checks`
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-checks` · `bin/probes/probe-checks.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ A check that has only ever been seen GREEN has not been tested.

⚠️ **The failure this prevents is not a missing check.** ⛔ **It is a check that is present,
active, trusted — and blind.** It runs, reports green, and is not measuring what it claims.

⭐ **This is the only rule in the folder that governs the OTHER rules' enforcement.** Every 🔒 in
every contract depends on the validator behind it actually measuring something.

### ⭐ WHY A BLIND CHECK IS WORSE THAN NO CHECK

| | ⭐ What happens |
|---|---|
| **no check** | ⚠️ the gap is visible — someone eventually notices and writes one |
| ⛔ **a blind check** | ⭐ **the gap is covered by a green.** Nobody looks again |

> ⛔ **False confidence is worse than a known hole.** A hole can be seen; a green that means
> nothing cannot.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `CHK-<area>-<nnn>` — ⛔ never renumbered, never reused.

⚠️ **This file is more 📖 than most, and that is honest:** ⭐ **a script can find a loose
comparison; it cannot know what a check meant to measure.**

---

## 2 · ⭐ THE RULE

> ## Before trusting a check, make it FAIL on purpose.

**Two runs, always:**

| Direction | The question |
|---|---|
| 🟢 **positive** | with the condition satisfied, does it pass? |
| 🔴 **negative** | ⭐ **breaking the condition deliberately, does it report it — and does the message name the REAL cause?** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-NEG-001` | ⭐ **Every check guarding something irreversible has a negative run** | 📖 | ⛔ nothing verifies this |
| `CHK-NEG-002` | ⭐ **The negative run leaves the state restored** | 📖 | ⚠️ a sabotage left behind is a defect you introduced |
| `CHK-NEG-003` | **Red for the wrong reason is not detection** | 📖 | ⭐ read the message, not the exit code |

⛔ **The negative run is the one that gets skipped**, and it is the only one that proves the check
is connected to what it claims to measure.

### ⭐ THE COROLLARY — a failed negative run may mean the PROBE is wrong

⚠️ **When a negative run does not fire, suspect BOTH the probe and the check.**

> ⛔ **Fixing only the probe leaves the hole — and you will have proven nothing while feeling that
> you did.**

⭐ **Measured twice in one session:** a probe removed one of two required mentions, so *"it did not
detect"* was a false negative **of the probe**. Investigating the probe is what exposed the real
defect underneath it.

---

## 3 · ⭐ THE VERDICT IS NOT BINARY

⛔ **"It failed" is not evidence that the check works.** ⚠️ **It may have failed for something
else entirely** — and a red for the wrong reason looks exactly like detection.

| Verdict | Means | ⭐ |
|---|---|---|
| ✅ **PASS** | the valid state was accepted | |
| 🔴 **FAIL** | ⭐ **the broken state was detected, and the message names the real cause** | ✅ the only red that counts |
| ⚠️ **WRONG_CAUSE** | ⛔ **it failed — for a different reason** | ⭐ the check is still unproven |
| 🔴 **CRASH** | ⛔ **it produced no verdict at all** | ⚠️ see below |
| ⬜ **SKIP** | it does not apply here, ⭐ **and it says so** | ⛔ never a pass |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-CAU-001` | ⭐ **A red counts only when the message names the intended cause** | 📖 | ⛔ read the message, not the exit code |
| `CHK-CAU-002` | 🔴 **A crash is not a detection** | 🔒 | ⭐ a validator that dies reports nothing |
| `CHK-CAU-003` | ⛔ **SKIP is said out loud, never counted as PASS** | 🔒 | ⚠️ a silent gap turned green |

### ⭐ WHY `CRASH` DESERVES ITS OWN NAME

⚠️ **A crashing validator produces no output — and "nothing reported" reads exactly like "nothing
wrong".** ⛔ **Measured twice while writing the validators in this folder:** one died on every
input including the correct one, and the sabotage run read it as *"detects nothing"*; ⭐ **the
truth was that it never ran at all.**

⭐ **So a validator catches its own exceptions and turns them into a finding with a non-zero
exit** — ⛔ **a stack trace is not actionable, and it is not a verdict.**

> ## ⭐ THE TEST FOR CAUSALITY
> ⛔ **Break a link → the validator crashes → FAIL.** ⚠️ **That does not prove it detects broken
> links. It proves the interpreter stopped.**

---

## 4 · ⭐ THE FIVE FAMILIES

⛔ **Every blind check measured so far falls into one of these.** ⭐ **When you find one, look for
the same shape in its siblings** — the pattern never lives alone.

### A · Loose comparison — the string is too short to mean anything

```
⛔  if id in text:              a short hex id matches inside a longer one
⛔  if number in text:          "016" is satisfied by "2016"
✅  match it with delimiters on both sides
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-CMP-001` | ⭐ **A short alphanumeric value is matched with delimiters** | 🔒 | ⛔ would an accidental occurrence make the system MORE permissive? |

⭐ **The test:** *if this string turned up by accident, would the system become more permissive?*
⚠️ **Short and alphanumeric → delimit it.** A literal with markup or a full path cannot appear by
chance and needs nothing.

### B · Short reach — the scope starts one level too low

```
⛔  walk from inside the subtree   → the file above it is never seen
⛔  a hardcoded list of files      → the newest one was never added
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-RCH-001` | ⭐ **The reach covers everything the check claims to protect** | 📖 | ⛔ see the test below |

⭐ **The test: name the thing this check protects. Now list what it actually reaches. The gap is
the finding.**

⚠️ **Measured, and it is the most ironic one:** ⭐ **the file read FIRST in every session was the
least watched** — because the search started one directory below it.

### C · Clobbered value — measured correctly, then overwritten

```
⛔  run; report "$(build_a_label)" "$?"      the substitution ate the exit code
✅  run; code=$?; report "..." "$code"
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-CLB-001` | ⭐ **A captured value is stored before anything else runs** | 🔒 | ⚠️ an exit status survives exactly one command |

⚠️ **This one hides for weeks:** ⭐ **when the expected value is zero, the clobbered value
coincides by accident** — so it passes, correctly, for the wrong reason.

### D · ⭐ Requiring something that BY DESIGN does not travel

```
⛔  require a directory that is deliberately not versioned
⛔  require a local-only settings file
✅  if it exists, hold it to the same standard · if not, say so and skip
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-TRV-001` | ⭐ **A check never requires a file that does not reach a clone** | 🔒 | ⛔ is it ignored, generated, or from another repository? |
| `CHK-TRV-002` | ⭐ **When the instance is absent, the check SKIPS and SAYS SO — never a pass** | 🔒 | ⚠️ a silent gap turned green is the false positive this rule exists to stop |

> ## 🔴 THE MOST EXPENSIVE FAMILY, MEASURED
> ⚠️ **A battery reporting all green on its author's machine, and failing many checks on a clean
> clone.** ⭐ **Nobody saw it for months because nobody ran it outside that one tree** — it was
> found by an external audit, not by the system.

⭐ **And the way out is never to stop verifying.** If the file exists, hold it to the same
standard; if it does not, ⭐ **verify the BEHAVIOUR instead** — *invoke the gate and require its
mark* verifies the same thing on any machine.

### D-bis · ⭐ The shape you cannot see: a RESULT that depends on the instance

⚠️ **These survive the first sweep because they name no missing file at all.**

| ⛔ The check | ⭐ What it actually required |
|---|---|
| opens a local-only file with no guard | ⛔ **it does not report a failure — it reports a crash** |
| looks for a literal directory name | ⚠️ on a clone the silence was CORRECT, and the check called it a failure |
| takes the exit code of a grader through a pipe | ⭐ **the GRADE that grader gives on its author's machine** |

> ## ⭐ THE LAST ONE IS THE WARNING THAT COVERS THEM ALL
> ⚠️ **No file is missing.** The tool runs, prints its output, and contains what the check looks
> for. ⭐ **What changes between machines is the SCORE** — and the score came in through the back
> door, as an exit code.
>
> ⛔ **A check can bind itself to one instance without naming it even once.**

⭐ **So the test widens:** besides *does this file reach a clone?*, ask ⭐ **would this NUMBER be
the same in an empty tree?** ⛔ **If it depends on how much work is done, the check is measuring
the work, not the system.**

### E · ⭐ Measuring the wrong shape — the check reads one form and the defect wears another

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-SHP-001` | ⭐ **The detector matches every shape the thing it measures can take** | 📖 | ⛔ count what it found · does the number look right? |

⚠️ **Measured while writing the validators in this folder, twice:** ⭐ **a detector that only
recognised one way of writing a rule reported ONE where there were seven** — and a duplicate
detector missed every copy, because ⭐ **a copy arrives in a different shape from the original.**

> ⛔ **A validator that measures a different thing from what it says it measures gives a green
> that means nothing** — and it is the hardest family to see, because the number it prints looks
> plausible.

⭐ **The test: does the count it reports match what you can count by hand?**

---

## 5 · ⭐ INSTANCE INDEPENDENCE — a rule, not just a family

> ## ⛔ THE LOCAL STATE OF ONE MACHINE MUST NOT BECOME PART OF THE SYSTEM'S SPECIFICATION.

⭐ **Family D describes the shape. This is the rule behind it**, and it is the one to apply before
writing a check, not after finding the defect.

| A check distinguishes… | |
|---|---|
| ⭐ **SYSTEM state** | what is true of the engine anywhere it is installed |
| ⛔ **INSTANCE state** | what happens to exist in this tree, on this machine |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-IND-001` | ⭐ **A check's verdict does not change with the amount of work already done** | 📖 | ⛔ would this be the same in an empty tree? |
| `CHK-IND-002` | ⭐ **Absent instance → verify the BEHAVIOUR instead** | 🔒 | ⚠️ not *"skip the check"* |
| `CHK-IND-003` | ⛔ **A check is proven on a clean clone, not only where it was written** | 📖 | ⭐ nothing verifies this yet |

⭐ **`CHK-IND-002` is what keeps this from becoming an excuse.** ⛔ **The way out is never to stop
verifying:** if the file exists, hold it to the same standard; ⭐ **if it does not, invoke the
thing and require its effect** — that verifies the same behaviour on any machine.

⚠️ **`CHK-IND-003` is 📖 and it is the most expensive gap in this file.** ⭐ **A validator proven
only where it was written has been proven on one instance** — and family D is exactly what that
produces.

---

## 6 · ⭐ THE COROLLARY THAT MULTIPLIES EVERY FINDING

> ## Fixing this family in one validator does NOT fix it in its siblings.

⚠️ **Measured four times in one day:** a validator carried the same defect that had already been
fixed in another. ⭐ **On finding one, search for the pattern in all the others.**

⭐ **It is the same question as the fix-not-patch rule, applied to the checks themselves:**
⛔ **not *"where does it fail?"* but *"why does this failure exist, and where else does it live?"***

---

## 7 · ⭐ THE ATTACK MATRIX — so the negative run is not improvised

⛔ **An agent inventing an attack each time produces a different battery every time** — ⚠️ some
checks get fifteen probes and others get six, ⭐ **and nothing says which coverage was intended.**

| The risk | ⭐ The attack that proves it |
|---|---|
| **loose comparison** | ⭐ introduce a partial match — a longer string containing the short one |
| **short reach** | move the target one level outside the search |
| **clobbered value** | insert a command between the run and the capture |
| ⭐ **instance dependence** | ⛔ **run it where the instance artifacts do not exist** |
| **instance-dependent result** | change how much work exists, ⭐ not whether files exist |
| **misleading exit code** | force a non-zero exit while the output still looks correct |
| **wrong shape** | ⭐ write the same defect in another valid form |
| **path dependence** | run it from a different working directory |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CHK-ATK-001` | ⭐ **Each attack that applies is run, or its absence is stated** | 📖 | ⛔ silence and *"not applicable"* look identical |

### ⭐ THE PROBE HAS ITS OWN FAILURE MODES — measured, three in a row

⚠️ **The file already says to suspect the probe. ⭐ What it did not say is HOW a probe fails**, and
there are three concrete shapes:

| # | ⛔ The probe… | ⭐ What it reports |
|---|---|---|
| 1 | **does not clean up everything it creates** | ⚠️ residue contaminates the next case, which then reports a stale finding as its own |
| 2 | ⭐ **its fixtures cannot reference each other** | a working graph check reported as broken |
| 3 | ⛔ **its output filter is narrower than what it generates** | ⭐ **a correct check reported as undetected** |

> ## ⭐ ALL THREE REPORT A WORKING CHECK AS BROKEN.
> ⛔ **That is the direction that costs most**, because the obvious response is to "fix" the check
> — ⚠️ **and then a working validator gets a defect introduced into it.**

---

## 8 · ⛔ WHAT THIS DOES NOT MEAN

| ⛔ Not this | ⭐ Why |
|---|---|
| **"delimit every comparison"** | ⚠️ a literal with markup cannot collide — **a validator that warns about non-defects is one people learn to ignore** |
| **"give every assertion a negative twin"** | ⛔ unaffordable, and it buries the ones that matter |
| ⭐ **"more checks is better"** | ⚠️ **a battery of 200 where 40 cannot fail is weaker than one of 160 where all can** |

⭐ **Scope it to what guards something IRREVERSIBLE:** data loss, credentials, a gate, anything
that cannot be undone.

⚠️ **And measure the scope rather than estimating it.** ⭐ **An estimate produces redundant probes,
and redundant probes are how a battery becomes noise.**

---

## 9 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **a check nobody has seen fail** | ⛔ ⭐ **it proves the check ran, not that it measures** |
| **a loose comparison** | ⚠️ an accidental match makes the system more permissive, silently |
| **short reach** | ⭐ the thing you most wanted to protect is outside the search |
| ⭐ **a check bound to one machine** | ⛔ **green here, broken everywhere else — and nobody finds out** |
| **fixing one sibling** | ⚠️ the same defect stays in the others, now with less suspicion on it |
| ⭐ **a red accepted without reading its cause** | ⛔ **the check is trusted for a failure it did not detect** |
| **a crash read as a detection** | ⚠️ ⭐ **it never ran, and nothing said so** |
| ⭐ **a defect in the PROBE fixed in the CHECK** | ⛔ **a working validator gets a defect introduced into it** |

---

## 10 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ which checks are in scope for a negative run | ⭐ the owner of the instance |
| the five families and their tests | whoever maintains the engine, through a recorded decision |
| ⛔ marking a check verified without a negative run | **nobody** — ⭐ ⚠️ **that is the exact defect this file exists to stop** |

---

Related: `README.md` (⭐ **the three enforcement levels — this rule is what makes a 🔒 honest**) ·
`rule-working-in-a-block.md` (⭐ §5 — *where else does it live*, the question that turns one
finding into four) · `../memory/principles/expertise/val-functional.md` (⭐ **§2.1 condition 3 and
§4 — the four conditions of evidence, and the procedure for proving a check can fail**) ·
`contract-document.md` · `../bin/check-checks` (what enforces the 🔒 rows).
