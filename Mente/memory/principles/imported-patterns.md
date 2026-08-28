# IMPORTED · failure patterns absorbed from outside

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Level:** 📖 catalogue — absorbed knowledge, ⛔ **not the owner's criterion**
**Scope:** ⚠️ ENGINE document — the patterns and their contract ship identical to every clone.

---

## Purpose

Failure patterns learned from outside this system and **rewritten as its own logic**.

> ## ⛔ THIS IS NOT THE OWNER'S CRITERION
> It is absorbed material — usable, but **not their judgement**. The owner's criterion lives in
> the discipline files. ⭐ **Mixing the two would launder someone else's opinion as the owner's**,
> which is the exact failure the "criterion is asked, never invented" rule exists to prevent.

⭐ **Why the distinction is worth a whole file:** a reader who finds an external rule inside a
discipline file will assume the owner decided it. Provenance is not bookkeeping — it is what makes
a criterion challengeable by the right person.

---

## 1 · ⭐ THE LAW OF ABSORPTION

> A failure pattern may be absorbed **only** when the failure can be stated independently of the
> source's implementation, and verified against this system's own stack.

⭐ **What is kept is the failure. What is dropped is the syntax.**

⛔ **The source is never named.** Not out of discretion — because naming it invites copying its
API, and its API is the half that does not transfer. ⚠️ **A file that accumulates *"what tool X
said"* becomes a graveyard of other people's architectures.**

⭐ **Three patterns absorbed honestly beat thirty copied blindly.** The count is not the metric:
a pattern nobody can detect is a sentence, not a rule.

---

## 2 · THE PATTERN CONTRACT

Every pattern below carries the same fields, in the same order. ⭐ **Uniformity is what lets a
script read this file** — an irregular catalogue can only ever be read by a person.

| Field | What it states |
|---|---|
| **ID** | ⭐ permanent. `FP-<area>-<nnn>` · never renumbered |
| **Failure** | what goes wrong, independent of any stack |
| **Why** | the consequence |
| **Detection** | ⭐ **how it is found** — static, runtime, or both |
| **Evidence** | what a finding must show |
| **Severity** | how bad it is when present |
| **Policy** | ⬜ what it does to shipping |
| **Remediation** | the steps that resolve it |

⛔ **The ID is an address, not a position.** Numbering by order means inserting one renumbers the
rest, and every reference to them breaks silently.

### Severity is not shipping policy

⭐ These are two decisions, and merging them removes one. Severity describes the defect; policy
describes what this installation does about it — and that is the owner's call.

| Severity | Means |
|---|---|
| 🔴 **critical** | security, silent data loss, or corruption |
| 🟠 **high** | fails under growth or load |
| 🟡 **medium** | correct today, fragile |

⬜ **Declare your policy per severity:** block · warn · inform.

### Result states

| State | Means |
|---|---|
| ✅ **PASS** | the pattern was looked for and is absent |
| 🔴 **FAIL** | the pattern is present, with evidence |
| ⚠️ **WARN** | present, but the condition that makes it critical is unmeasured |
| ⬜ **UNKNOWN** | ⭐ **it could not be checked** |
| 🔓 **EXEMPTED** | present, with an approved exception (§4) |

> ## ⛔ UNKNOWN IS NOT PASS
> *"No index was found"* and *"there is no index"* are different statements. ⭐ **Absence of
> evidence is not evidence of correctness** — and a catalogue that conflates them reports green
> for everything it failed to inspect.

---

## ⭐ 2b · WHEN A PATTERN AND A CRITERION SAY THE SAME THING

⚠️ **Several patterns here restate a criterion that lives in `expertise/`.** That is not
duplication to remove — ⭐ **they are different layers, and the difference decides what you do.**

| | Says | ⛔ Cannot |
|---|---|---|
| **a criterion** in `expertise/` | ⭐ **what must be true** — it is judged | be run |
| **a pattern** here | ⭐ **what the defect looks like** — it is detected | judge a design |

⭐ **A criterion rejects a design; a pattern finds an instance.** `FP-SEC-001` is the detectable
shape of `expertise/dev-backend.md` §2.5 (`BE-CON-005`); `FP-SEC-002` is the shape of
`expertise/dev-frontend.md` §2.5 (`FE-SEC-002`).

> ## ⛔ THE CRITERION IS THE AUTHORITY. THE PATTERN IS THE DETECTOR.
> ⚠️ **On disagreement, the criterion wins** — a pattern is an absorbed observation, and
> `expertise/val-integration.md` §7 already says a precedent does not outrank a rule.

⭐ **When a pattern has no criterion behind it, that is the finding**: either the criterion is
missing from a discipline, or the pattern was never criterion at all.

---

## 3 · THE PATTERNS

### FP-SEC-001 · Authorisation from a client-supplied identity

- **Failure:** the request states who it is, and the query believes it
- **Why:** ⭐ anyone impersonates anyone by passing the right identifier
- **Detection:** static — does the authorisation path read a request field, or the verified session?
- **Evidence:** file · line · the field it read · the session field it should have read
- **Severity:** 🔴 critical — ⭐ **a security finding, never a performance one**
- **Remediation:** resolve identity from the verified session · perform the ownership check ·
  add a regression test that passes a foreign identifier and expects a refusal

⚠️ **A schema constraint cannot catch this** — it cannot tell a legitimate identifier from a
spoofed one. That is why it lives in criterion and not in a validator.

### FP-SEC-002 · A client-side guard as the only guard

- **Failure:** the interface hides an action, and nothing on the server refuses it
- **Why:** ⭐ hiding a control is presentation, not authorisation — the endpoint is still callable
- **Detection:** static — for each hidden action, does a server-side check exist?
- **Evidence:** the hidden control · the endpoint · the absence of the check
- **Severity:** 🔴 critical
- **Remediation:** every hidden action gets its check on the server. The interface may still hide
  it — ⭐ **hiding is courtesy, refusing is security**

### FP-PERF-001 · Filtering on a column with no index

- **Failure:** a full scan on every query
- **Why:** fine at ten rows, a timeout at a hundred thousand
- **Detection:** ⭐ **static + runtime** — the columns in the filter, the schema's indexes, and
  the measured row count
- **Evidence:** the query · the column · the indexes present · ⭐ **the row count, measured**
- **Severity:** 🟠 high on a table expected to grow · 🟡 medium on a bounded one
- **Remediation:** add the index, or declare the table bounded as an exception (§4)

⭐ **The severity depends on a measurement, so the finding states the count.** ⛔ Never assumed —
"it is a small table" is the sentence that precedes the timeout.

### FP-PERF-002 · Reading a whole collection with no bound

- **Failure:** *"give me everything"*
- **Why:** works today, exhausts memory when the data grows
- **Detection:** static — a read with no limit
- **Evidence:** the call · whether a bound exists · the measured size
- **Severity:** 🟠 high on unbounded data · 🟡 medium on bounded
- **Remediation:** paginate, or bound explicitly and say why the bound is safe

### FP-SILENT-001 · Not awaiting an asynchronous write

- **Failure:** the write is issued and never waited on
- **Why:** ⭐ **it fails silently — no error, no data, and a log that looks clean**
- **Detection:** static — an async call whose result is discarded
- **Evidence:** file · line · the discarded call
- **Severity:** 🔴 critical — silent data loss
- **Remediation:** await it and handle its failure. ⛔ Discarding the result is a decision that
  must be written down, not implied

### FP-SILENT-002 · Sequential writes where one transaction belongs

- **Failure:** several writes that must succeed together, issued separately
- **Why:** a failure between them leaves inconsistent intermediate state, and nothing reports it
- **Detection:** static — consecutive writes with no transaction boundary
- **Evidence:** the writes · the invariant they jointly maintain
- **Severity:** 🔴 critical
- **Remediation:** one transaction. ⚠️ If the store has no transactions, the intermediate state is
  a declared and documented risk, not an oversight

### FP-SILENT-003 · Reading the clock inside a cached read

- **Failure:** current time evaluated inside something that is cached
- **Why:** ⭐ the value freezes at first evaluation and serves stale data forever after
- **Detection:** static — a time call inside a cached path
- **Evidence:** the call · the cache that contains it
- **Severity:** 🔴 critical — the failure is invisible: the data looks valid, only old
- **Remediation:** ⭐ a time-based transition belongs to a scheduled job that **writes** state, so
  the read filters by that state instead of computing it

### FP-STATE-001 · Deriving state the server already owns

- **Failure:** the client recomputes what the server decided
- **Why:** the two drift, and neither is marked wrong
- **Detection:** static — a client-side computation of a value the server returns
- **Evidence:** both values · ⭐ **the divergence, measured**
- **Severity:** 🟡 medium — 🔴 critical once a divergence is observed
- **Remediation:** the server owns the truth, the client renders it

### FP-STATE-002 · Refetching by hand after a write

- **Failure:** a manual re-read after writing, when the data layer already propagates
- **Why:** duplicates the source of truth and races the real update
- **Detection:** static — a read immediately following a write on the same data
- **Evidence:** the write · the refetch · whether propagation exists
- **Severity:** 🟡 medium
- **Remediation:** trust the propagation. ⭐ **If there is none, say so explicitly** — an
  undocumented manual refetch looks identical to a bug

### FP-STRUCT-001 · Circular imports through a shared module

- **Failure:** two modules import each other through a common one
- **Why:** ⭐ passes static analysis and fails at runtime with an undefined reference
- **Detection:** static — the import graph
- **Evidence:** the cycle, named in order
- **Severity:** 🟠 high
- **Remediation:** extract the shared part, or invert one dependency

---

## 4 · ⭐ EXCEPTIONS — and they need evidence too

Some patterns are correct to leave in place. ⛔ **But an exception with no evidence is just an
opinion that outranks a rule.**

| Field | Required |
|---|---|
| the pattern ID | which rule is being excepted |
| ⭐ **the measurable condition** | what makes it safe **here** |
| the measurement | the value observed, and when |
| who approved it | ⭐ the owner — never the agent |
| when it is re-checked | ⚠️ or `never`, stated on purpose |

⭐ **Not *"the owner said it is fine"* — but *"the owner approved it because this measurable
condition holds"*.** The first cannot be re-evaluated when the condition changes; the second
becomes wrong on its own, loudly, the day the measurement moves.

⚠️ **An exception with no re-check date on data that can grow is a rule that was deleted with
extra steps.**

---

## 5 · WHERE THIS SITS

```
owner criterion          ⭐ the discipline files — the owner's judgement
      │
      ▼
absorbed patterns        THIS FILE — knowledge, not judgement
      │
      ▼
detection                how each is found
      │
      ▼
evidence                 what a finding must show
      │
      ▼
severity → ⬜ policy      what it does to shipping
```

⛔ **These patterns never replace the discipline criterion.** They are a floor of known failures,
not a definition of good work. ⭐ **A change that trips none of them can still be rejected** — by
the owner's criterion, which is a different and higher bar.

---

## 6 · ⭐ WHO GOVERNS THIS FILE

| Change | Who may make it |
|---|---|
| the shipping policy per severity, and the exceptions | ⭐ the owner of the instance |
| absorbing a new pattern | whoever maintains the engine — ⚠️ **only if it passes §1** |
| ⛔ moving a pattern into a discipline file | **never** — that would relabel absorbed knowledge as the owner's criterion |

---

Related: `README.md` (⭐ **the parent — read it for context**) · the discipline files under
`expertise/` (⭐ **the owner's criterion, which these never replace**) · `owner-2-dev.md` (what
loads them) · `owner-3-validation.md` (evidence and result states) ·
`../../docs/ENGINE-BACKLOG.md`.
