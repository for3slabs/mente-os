# RULE · CONFIGURATION HYGIENE

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every configuration file that grants a permission or registers a gate
**Enforcement:** 🔒 partial — `bin/check-config`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone
**Size:** ⭐ **a BASE file — it ships whole.** See `contract-document.md` §4.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The six rules that keep a permission surface from becoming a hole nobody can see.

⚠️ **The configuration that registers the gates is the highest-leverage file in a project** — it
decides what blocks, what warns, and what is injected before an edit. ⛔ **And it is the file least
likely to be reviewed**, because nothing about it looks like code.

### 🔴 THE MEASUREMENT THAT NAMED THIS FILE

⚠️ **A file with this exact name already existed — and it was about something else.** ⭐ **The real
configuration rules were buried inside a long architecture document.**

⛔ **So an audit re-derived, from scratch, the exact criteria that were already written** — because
the file whose name promised them did not contain them.

> ## ⭐ A NAME THAT LIES IS A FILE THAT DOES NOT GET READ.
> ⚠️ **The rules existed. The mechanism that would surface them did not** — and that is the shape
> of every failure in §8.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `CFG-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · 🔴 SECRETS ARE REFERENCED, NEVER PASTED

```
⛔  <command> --password '<the real value>'
✅  <command> --password "$AN_ENVIRONMENT_VARIABLE"
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-SEC-001` | 🔴 **No secret in an approved command** | 🔒 | ⛔ see below |
| `CFG-SEC-002` | 🔴 **No secret in a configuration file** | 🔒 | ⚠️ not even a placeholder that once held one |
| `CFG-SEC-003` | ⭐ **A leaked secret is ROTATED, never just deleted** | 📖 | ⛔ purging does not invalidate |

### ⭐ WHY THIS IS A RULE AND NOT ADVICE

⛔ **Approving a command files it VERBATIM as a permanent permission.** ⚠️ **A secret pasted into
an approved command is recorded forever** — not once, but every time it is approved again.

⭐ **Measured: hundreds of stored entries carrying the same credential**, in a file that was not
excluded from version control.

| Where a secret may live | |
|---|---|
| the secrets store | ✅ excluded from version control |
| an environment variable | ✅ ⭐ never on disk |
| ⛔ **an approved command** | 🔴 **forbidden** |
| ⛔ **a configuration file** | 🔴 **forbidden** |

> ## ⚠️ PURGING DOES NOT INVALIDATE
> ⭐ **A secret removed from a file still lives in every transcript that recorded it** — and
> transcripts are not edited. ⛔ **Any leaked secret is ROTATED. Deleting it only hides it.**

---

## 3 · ⭐ EVERY GRANTED PATH DECLARES ITS WHY

⚠️ **A path is granted once and inherited forever.** ⛔ **Nobody removes one they cannot explain,
because removing it might break something** — so it stays, unexplained, until it is load-bearing.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-WHY-001` | ⭐ **Every granted path states why it exists** | 🟡 | ⛔ and when it was added |
| `CFG-WHY-002` | ⭐ **A path nobody can justify is REMOVED** | 🟡 | ⚠️ see below |
| `CFG-WHY-003` | **A granted path resolves** | 🔒 | ⭐ a dead path is a grant nobody uses and nobody audits |

⭐ **Measured when this rule was written: nine granted paths, NONE justified.** ⚠️ **Three pointed
at directories that did not exist; one contradicted a gate the same configuration declared.**

> ## 🔴 THE ONE THAT PROVES THE RULE
> ⚠️ **A grant reaching the system's device tree was removed the day this table was written.**
> ⛔ **No document, rule or record said why it had been added.**
>
> ⭐ **A path nobody can justify is a path that goes** — that is what "the why is required" means:
> ⛔ **required, not decorative.**

⭐ **Where the why lives is the installation's choice** — ⬜ inline if the format allows comments,
in a declared table if it does not. ⚠️ **What is not optional is that it exists.**

---

## 4 · ⭐ ONE MECHANISM, ONE ENTRY

> ## ⭐ Does this entry authorize something NO other entry already authorizes?
> ⛔ **If not, it does not go in.**

| # | Criterion | ⚠️ Measured |
|---|---|---|
| 1 | ⭐ **No overlap** — if one contains another, the narrower does not enter | a directory already contained its own subdirectory |
| 2 | **No dead paths** | ⛔ a third of them did not exist |
| 3 | 🔴 **One entry per MECHANISM, never per invocation** | ⭐ see below |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-ONE-001` | ⭐ **An entry that grants nothing new does not enter** | 🔒 | `bin/check-config` · a path contained by another, and the SAME command written two ways |
| `CFG-ONE-002` | 🔴 **The granularity is the MECHANISM, not the invocation** | 🔒 | `bin/check-config` · grouped by the SCRIPT, never by the first path segment |

### ⚠️ THE SHAPE THAT HIDES: ONE COMMAND, TWO SPELLINGS

⛔ **Measured in a real configuration: 14 commands granted twice** — once as `x` and once as
`./x`. ⚠️ Nobody added a capability; somebody approved the same one from a different working
directory, and the list grew by 14 without granting anything.

> ## ⭐ THE DUPLICATE THAT SURVIVES IS THE ONE THAT DOES NOT LOOK LIKE A DUPLICATE.
> ⛔ **A grouping that reads the first path segment reports one mechanism with 15 entries when it
> is 15 scripts** — the count is right, the cause is wrong, and a wrong cause sends the fix to
> the wrong place.

### 🔴 WHAT "PER INVOCATION" LOOKS LIKE, MEASURED

⚠️ **Over a thousand stored permissions, grouped by mechanism, collapsed to a handful:** ⛔ **more
than two hundred entries for ONE tool, over a hundred for another.**

> ## ⭐ TWO HUNDRED ENTRIES FOR "MAY USE THIS TOOL" IS NOT A PERMISSION LIST.
> ⛔ **It is a log of every time somebody said yes.**

⚠️ **And a list nobody can read is a list nobody audits** — ⭐ which is how the entries that
actually deserve review end up invisible among the ones that do not.

---

## 5 · ⭐ PORTABLE PATHS

⚠️ **Measured: hundreds of absolute paths pointing at one person's home directory.** ⛔ **Nobody
else can use that configuration** — and nothing said so.

| ⛔ Not portable | ✅ Portable |
|---|---|
| an absolute path into somebody's home | ⭐ a path relative to the project root |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-PRT-001` | ⭐ **A path is written relative to the project** | 🟡 | ⛔ an absolute one measures one machine |
| `CFG-PRT-002` | ⭐ **A genuinely non-portable path is DECLARED as such** | 📖 | ⚠️ see below |

> ## ⭐ A DECLARED LIMIT IS ENGINEERING. A HIDDEN ONE IS DEBT.
> ⚠️ **Some integrations are external and carry their own absolute paths.** ⛔ **Pretending they
> are portable is the defect** — ⭐ **saying they are not is the fix.**

---

## 6 · 🔴 THE PROTECTED SURFACE IS DECLARED COMPLETE, NOT PER TOOL

⚠️ **A protection covered the read, edit and write tools. It did not cover the shell.** ⛔ **So an
ordinary shell command read exactly what the protection forbade.**

⭐ **Proven live, before the fix:** listing a protected directory succeeded with zero friction —
⚠️ **a directory under an explicit denial.**

> ## 🚫 A PROTECTION DECLARED BY TOOL IS A PROTECTION WITH A BACK DOOR.
> ⛔ **The question is not *"did I deny the read tool?"*** — ⭐ **it is *"can ANYTHING still reach
> it?"***

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-SUR-001` | 🔴 **Every reach channel to a protected target is denied** | 🔒 | ⛔ see the channel table |
| `CFG-SUR-002` | 🔴 **The guard DISCOVERS what is protected — it does not consult a list** | 🔒 | ⭐ §7 |
| `CFG-SUR-003` | ⛔ **A shell wrapper grant makes every other denial decorative** | 🔒 | ⚠️ see below |

### ⭐ THE CHANNELS — a protected target is reachable by more than one

| Channel | ⭐ What must be covered |
|---|---|
| **read** | the ordinary readers and pagers |
| ⭐ **binary read** | ⚠️ **the ones that read a file without "reading" it** |
| **copy out** | ⛔ copy, move, archive — ⭐ **a target copied elsewhere is no longer protected** |

⚠️ **The copy channel is the one that gets forgotten**, and it is the worst: ⭐ **the protection
still reports as intact while the content sits somewhere unprotected.**

### 🔴 THE TWO GRANTS THAT MAKE EVERY DENIAL DECORATIVE

⛔ **A grant for a shell interpreter itself.** ⚠️ **With one of those approved, any command runs by
wrapping it** — ⭐ **and every specific denial in the list becomes a suggestion.**

⭐ **Also worth denying outright: a recursive delete with no path.** ⚠️ Measured as authorized,
unrestricted.

### ⭐ WHY THIS RULE WAS INVISIBLE

⚠️ **The other five all check the SHAPE of the permissions** — are they justified, portable,
deduplicated, secret-free. ⛔ **None of them asks whether the surface has a hole.**

> ## ⭐ A CONFIGURATION CAN BE PERFECTLY TIDY AND STILL WIDE OPEN.

---

## 7 · ⭐ A LIST THAT ENUMERATES WHAT IS PROTECTED MUST BE MEASURED

⚠️ **The first version of this rule said "no fixed lists". That was too broad** — ⭐ most
enumerations in a validator are correct, and several are correct **on purpose.**

> ## ⭐ THE SHARPER RULE
> **A list that enumerates what is PROTECTED must be MEASURED.**
> **A list that enumerates what is PERMITTED may be written — ⭐ if the unknown fails CLOSED.**

| The list enumerates | On something it does not know | Verdict |
|---|---|---|
| ⛔ **the protected** — what must not be reached | ⚠️ **stays silent** | 🔴 **it bit** |
| ⛔ **what is being watched** | never checked it | 🔴 **it watched a fraction** |
| ✅ **the permitted** | ⭐ **blocks** | ✅ safe by design |
| ✅ **a closed vocabulary** | rejects | ⭐ a new value is a decision, not a discovery |
| ✅ **known exceptions** | a false positive | ⚠️ noise, ⛔ never a hole |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-LST-001` | 🔴 **A list of the PROTECTED is discovered, never written** | 🔒 | ⛔ it must find what exists |
| `CFG-LST-002` | ⭐ **A list of the PERMITTED fails CLOSED on the unknown** | 🔒 | ⚠️ otherwise it is a list of the protected in disguise |

> ## ⭐ THE TEST BEFORE WRITING ANY LIST
> **If this list is short by one, does the system become more PERMISSIVE or more STRICT?**
> ⛔ **More permissive → it must be measured.** ✅ More strict → writing it is fine.

### 🔴 A FIXED LIST OF WHAT IS DANGEROUS IS A HOLE WITH A SCHEDULE

⚠️ **Measured: a guard for exactly this failure stayed silent, because it consulted a hardcoded
list of three targets** — ⛔ **and the credentials it missed were sitting in plain reach.**

⭐ **The same shape hit three times in one day:** a denial covering three tools but not the fourth ·
a test counting exactly three rules per target · a list of three protected paths. ⚠️ **In all
three the guard reported green with the hole wide open.**

> ## ⭐ WHEN A CHECK ENUMERATES, ASK WHAT THE ENUMERATION LEAVES OUT.

---

## 8 · ⭐ DENIALS ARE SHARED, GRANTS ARE NOT

| File | Travels | ⭐ What belongs there |
|---|---|---|
| **the shared configuration** | ✅ yes | ⭐ **the gates · every DENIAL · the shared minimum** |
| **the local configuration** | ⛔ excluded | ⚠️ machine-specific approvals only |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-SHR-001` | 🔴 **Every denial is mirrored into the shared file** | 🔒 | ⛔ see below |
| `CFG-SHR-002` | ⭐ **Grants stay asymmetric on purpose** | 📖 | ⚠️ they are per machine |
| `CFG-SHR-003` | ⭐ **The broad grants are the ones that need review** | 🟡 | ⛔ and they hide in the unaudited file |

> ## 🔴 A DENIAL THAT LIVES ONLY IN THE LOCAL FILE PROTECTS NOBODY ELSE.
> ⚠️ **Measured: a handful of shared grants against two hundred local ones.** ⛔ **Anyone opening
> the project elsewhere starts with a fraction of the permissions** — ⭐ **and the broad wildcards,
> the ones that actually deserve review, lived in the file nobody audits.**

---

## 9 · ⭐ THE PATTERN BEHIND EVERY MEASURED FAILURE

| The failure | ⭐ The convention existed | ⛔ What was missing |
|---|---|---|
| a credential stored hundreds of times | ⭐ the secrets store was the right place | **nothing forced referencing it** |
| hundreds of unportable paths | — | ⛔ **nothing demanded portability** |
| a grant contradicting a gate | ⭐ the gate forbade it | **nothing asked the path to justify itself** |
| the shell reading past a denial | — | ⛔ **nothing asked if the surface was complete** |
| ⭐ **these rules re-derived from zero** | ⭐ **they were written** | ⛔ **the file named for them held something else** |

> ## ⭐ IN ALL FIVE, THE RULE EXISTED OR WAS OBVIOUS. WHAT WAS MISSING WAS THE MECHANISM.
> ⚠️ **And in the last one, the mechanism was as simple as a filename that told the truth.**

⭐ **That is why every row of this file names what enforces it** — ⛔ and why the ones marked 📖 say
so instead of implying otherwise.

---

## 10 · 🔴 A THRESHOLD MISSED BY ONE IS A THRESHOLD SET BY ACCIDENT

⚠️ **A count-based check fired above a round number. The real count sat one unit below it** —
⛔ **so it never spoke, while the situation it existed to catch was fully present.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CFG-THR-001` | ⭐ **A threshold is derived from what is acceptable, not from a round number** | 📖 | ⛔ nothing verifies this |
| `CFG-THR-002` | ⚠️ **A threshold never crossed is re-examined, not trusted** | 📖 | ⭐ see `rule-checks-must-measure.md` §2.6 |

⭐ **A limit set where nothing has ever reached is not protecting anything** — ⚠️ **and it reports
green for exactly as long as it is useless.**

---

## 11 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **a secret in an approved command** | ⛔ ⭐ **recorded forever, and deleting it does not invalidate it** |
| **an unjustified path** | ⚠️ nobody removes what they cannot explain — ⭐ it becomes load-bearing |
| **one entry per invocation** | ⛔ a list nobody reads is a list nobody audits |
| **an absolute path** | ⭐ the configuration measures one machine |
| ⭐ **a protection declared per tool** | 🔴 **a back door that reports as protected** |
| **a written list of what is protected** | ⛔ ⭐ **a hole with a schedule** |
| **a denial only in the local file** | ⚠️ it protects nobody else, and nothing says so |
| ⭐ **a shell wrapper granted** | ⛔ **every other denial becomes decorative** |
| **a threshold set at a round number** | ⭐ green for exactly as long as it is useless |

---

## 12 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ which paths are granted, and their reasons | ⭐ the owner of the instance |
| ⬜ the thresholds | the owner, ⚠️ **derived, never rounded** |
| the six rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ pasting a secret "just for a test" | **nobody** — ⭐ ⚠️ **the record does not distinguish tests** |
| ⛔ writing a list of what is protected | **nobody** — ⭐ §7 |

---

Related: `README.md` (⭐ the three document types) · `rule-checks-must-measure.md` (⭐ **the sibling
rule — this one governs LISTS, that one the other ways a check goes blind**) ·
`contract-document.md` (⭐ §9 — no credential, not even as an example) · `contract-archive.md`
(⭐ §6 — and not in an archive either) · `rule-shipping.md` (⭐ §10 anti-pattern 7) ·
`../bin/check-config` (what enforces the 🔒 rows).
