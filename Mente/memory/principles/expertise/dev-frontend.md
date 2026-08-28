# EXPERTISE · FRONTEND

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-2-dev.md` — development
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §0 to §2, §4 and §5 ship identical; §3 is yours.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ FRONTEND = REPRESENTATION + INTERACTION + TRUST

An interface is not decoration. It is **the only thing the user can see of a system they cannot
inspect** — so it does three jobs at once, and the third is the one that gets forgotten:

| | The job | If it fails |
|---|---|---|
| **represents** | shows what the system's state actually is | the user reasons about a system that does not exist |
| **interacts** | accepts an action and reports what happened to it | the user does not know if anything occurred |
| ⭐ **protects trust** | never claims something the system does not know is true | ⛔ **everything else becomes unverifiable** |

> ⭐ **Why frontend needs a principle the other disciplines do not:** in backend, a defect
> *announces itself* — something breaks, a request fails, a log fills. **In frontend a defect
> looks fine.** A button reading "saved" after a failed request does not look broken; it looks
> correct. ⛔ **That is why truth has to be a principle here and not one criterion among others.**

### Two things live here, and they must never be confused

| | |
|---|---|
| **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
| **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |

### ⛔ DO NOT INVENT

| Situation | ⭐ The response |
|---|---|
| the criterion does not exist | **ask** — ⛔ never fill the gap with "best practices" |
| the criterion exists, the evidence does not | ⬜ **declare UNKNOWN** |
| something is built but not connected | ⭐ **declare the seam** |
| there is evidence of a violation | 🔴 block |

---

## 1 · ⭐ PRINCIPLE ZERO · UI TRUTH

> ## ⛔ THE INTERFACE NEVER CLAIMS ANYTHING THE SYSTEM DOES NOT KNOW TO BE TRUE.

Everything below derives from that one sentence:

| Derived rule | Means |
|---|---|
| **the server's state wins** | when the interface and the system disagree, the interface is wrong |
| **a failed action is not a success** | ⛔ never report completion the system did not confirm |
| **loading is not idle** | *"nothing is happening"* and *"something is happening"* look identical if unsaid |
| ⭐ **`unknown` is not `false`** | ⚠️ see below — the most missed of the seven |
| **hidden is not authorised** | hiding a control is presentation; refusing is security |
| **persisted survives a refresh** | if it does not survive, it was never persisted |
| **optimistic state reconciles** | ⭐ what was shown before confirmation is corrected when it arrives |

### ⭐ `unknown` is not `false`

When the system cannot determine a state, the interface says **so** — it does not pick the
convenient value.

```
⛔  the status endpoint is unreachable  →  shows "off"
✅  the status endpoint is unreachable  →  "status unavailable · retry"
```

⚠️ **Reporting `unknown` as `false` is a lie that looks like a normal reading.** The user acts on
it, and nothing anywhere reports that the answer was invented.

### ⭐ THE HIERARCHY OF REJECTION

| Level | Problem | Costs |
|---|---|---|
| 🔴 **the interface lies** | it shows a state the system knows is different | ⭐ **trust — and trust does not come back with a fix** |
| 🟠 **no feedback** | the user cannot tell whether it is working or failed | usability |
| 🟠 **two ways to do one thing** | duplicated paths with no criterion for choosing | coherence |
| 🟡 **it breaks when resized** | gaps, cut content | it looks unfinished |

⭐ **The bottom three make a product look unfinished. The first makes it untrustworthy.** They are
not the same class of defect, and treating them as one is how the expensive one gets deprioritised
behind the visible one.

---

## 2 · THE BASE STANDARD

### 2.1 · ⭐ Where state lives — four kinds, not one

*"The server owns the state"* is true and incomplete. ⛔ **Not all state is the server's**, and
putting everything in one place is as wrong as scattering it.

| Kind | Examples | Lives in | ⚠️ The failure |
|---|---|---|---|
| **server** | the session, the data, permissions | ⭐ the server decides; the client renders | duplicating it client-side, and the two drift |
| ⭐ **URL** | page, filter, ordering, what is open | **the address** | ⚠️ the view cannot be shared, bookmarked, or restored by reload |
| **form** | what the user typed, not yet sent | the form, until it is submitted | ⛔ **losing it on an error** |
| **ephemeral** | hover, an open menu, an animation | the client — ✅ and that is correct | promoting it to persistent for no reason |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `FE-STA-001` | ⭐ **State that must survive a reload has a persistent home** | 🔴 | act · reload · compare what is shown against the system |
| `FE-STA-002` | ⭐ **A view worth returning to is addressable** | 🟠 | can it be reached by its address alone? |
| `FE-STA-003` | ⛔ **A failed action never discards what the user wrote** | 🔴 | trigger the failure with the field filled in |
| `FE-STA-004` | **One value, one owner** — the client does not recompute what the system decided | 🟠 | is the same value derived in two places? |

⭐ **`FE-STA-002` is the one nobody implements and everybody misses.** A filter, a tab, an open
panel — if the address does not carry them, the user cannot share what they are looking at, and a
reload throws them back to the beginning.

### 2.2 · Interaction — every action has a shape

⭐ **An action is never just "it happens".** It has a before, a during, and two possible afters:

```
idle → pending ─┬─ success
                └─ error → retry
```

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `FE-INT-001` | ⭐ **Every action reports that it started** | 🟠 | click and observe: does anything change? |
| `FE-INT-002` | **Every action reports how it ended** — success or failure, distinguishably | 🔴 | force each outcome and observe |
| `FE-INT-003` | **A failure says what can be done next** | 🟠 | ⛔ *"an error occurred"* is not a next step |
| `FE-INT-004` | ⭐ **Optimistic state reconciles with the answer** | 🔴 | make the server refuse, and observe whether it reverts |
| `FE-INT-005` | ⭐ **Out-of-order answers do not win** | 🟠 | two actions in sequence, answers reversed — does the last one shown match the last one sent? |
| `FE-INT-006` | **A repeated action does not duplicate its effect** | 🟠 | act twice quickly |

⚠️ **`FE-INT-005` is a real defect that looks like a rare one.** Two requests, answers arriving
reversed, and the interface shows the older result as if it were current. ⭐ **It is concurrency,
and it lives in the client too.**

### 2.3 · The states a screen must cover

⛔ **A screen that only handles the happy path is not finished.** For each one, either there is a
defined behaviour, or it is stated as not applicable:

| State | The question |
|---|---|
| **initial** | before anything loads |
| **loading** | ⭐ and whether it blocks everything, or only the part that is waiting |
| **success** | with data |
| ⭐ **empty** | ⛔ zero results is not the same as loading — and an empty area explains nothing |
| **error** | with a way forward |
| **unauthorised** | ⭐ ⚠️ different from empty, and different from error |
| **stale** | the data may no longer be current |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `FE-STE-001` | **Every applicable state has a defined behaviour** | 🟠 | walk them one by one |
| `FE-STE-002` | ⭐ **Empty explains why it is empty and what can be done** | 🟠 | is it a blank area, or a message? |
| `FE-STE-003` | ⛔ **Loading does not freeze what did load** | 🟠 | partial load: is the rest usable? |

### 2.4 · Architecture — one responsibility per piece

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `FE-ARC-001` | ⭐ **A piece that renders does not also decide** | 🟠 | does it paint, fetch, transform **and** decide? Then it is four pieces |
| `FE-ARC-002` | **A piece runs on the client only if it needs to** — interaction, browser capability, local state | 🟠 | which of the three does it need? If none: it does not belong there |
| `FE-ARC-003` | **Equivalent components behave equivalently** | 🟠 | ⭐ do two buttons show *loading* differently? |

⭐ **`FE-ARC-003` is invisible one piece at a time and obvious across a product.** When each
control invents its own way of waiting, the user relearns the interface on every screen.

### 2.5 · Abstraction, naming, necessity

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `FE-ABS-001` | **Repeated three times with the same meaning → one piece** | 🟠 | ⚠️ the same **meaning**, not the same shape |
| `FE-ABS-002` | ⛔ **Do not abstract because two things look alike** — abstract when they must change together | 🟠 | would a change to one require the same change to the other? |
| `FE-ABS-003` | **Visual values come from the system that defines them**, not invented per case | 🟢 | do the spacings and sizes belong to the declared scale? |
| `FE-NAM-001` | ⭐ **The name says what it represents, not what it looks like** | 🟠 | ⛔ a name describing a colour or a position dies at the first redesign |
| `FE-NEC-001` | **What nobody uses is removed** | 🟠 | measure actual use — ⛔ *"it might be needed"* is not evidence |

### 2.6 · The client has no authority

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `FE-SEC-001` | ⛔ **No secret reaches the client** — keys, tokens, credentials | 🔴 | inspect what actually ships |
| `FE-SEC-002` | ⭐ **Hiding a control is not authorisation** | 🔴 | call the operation directly, with the control hidden |
| `FE-SEC-003` | **Anything the user supplies is treated as hostile** | 🔴 | what happens if the content is markup or a script? |
| `FE-SEC-004` | ⛔ **Sensitive data is not left where the browser keeps it** | 🔴 | inspect local storage |

⭐ **`FE-SEC-002` is the one that gets argued.** The argument is always *"the button is not
visible"*. **The endpoint is.**

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here**, using the model of §2 and ⭐ **your own prefix** — for example `FE-OWN-001`.
**Which criterion came with the engine and which you added must never require reading history.**

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** ⭐ **The AI asks, you answer with real cases, the AI
> structures.** Never the reverse — an invented interface criterion reads exactly like a real one.

**The questions that elicit it — answer with cases, not principles:**

1. What is the last interface you rejected, and what was wrong with it?
2. ⭐ What have you seen an interface claim that was not true?
3. What do you check first when you open someone else's screen?
4. What makes you say *"this looks unfinished"*?
5. What does your stack make easy that usually produces a bad interface?

---

## 4 · ⭐ THE PROTOCOL — before building a screen

⛔ **A question left unanswered here is a decision made by accident.** ⚠️ The ones that do not
apply are stated as not applying — ⭐ skipping silently and not applying look identical afterwards.

### What it represents

1. What does this screen show, and where does that come from?
2. ⭐ **Who owns each value shown** — the server, the address, the form, or the moment?
3. What must survive a reload, and what may be lost?

### What the user can do

4. What actions exist here?
5. For each one: what does the user see **while it runs**?
6. ⭐ **And when it fails — what can they do next?**
7. Is anything shown before the system confirms it? ⭐ **Then how is it corrected if refused?**
8. What happens if the same action is triggered twice?
9. ⭐ **What happens if two answers arrive out of order?**

### What it looks like when there is nothing, or something is wrong

10. What is shown before data arrives?
11. ⭐ **What is shown when there is none** — and does it say why?
12. What is shown when it fails?
13. What is shown when the user may not see it?
14. ⭐ **What is shown when the state cannot be determined?**

### Beyond one screen size and one input

15. How does it behave at the sizes it must support? ⭐ **Not shrunk — rearranged**
16. Can it be operated without a pointing device?
17. ⛔ Does anything communicate its meaning **only** through colour?
18. Can the view be returned to by its address?

### Trust

19. ⛔ What of this must never reach the client?
20. Is any control hidden as though hiding were a permission check?
21. ⭐ **Is there anywhere the interface could claim something the system has not confirmed?**

### Proof

22. How is each of the above demonstrated, rather than asserted?
23. ⭐ **Has the failure path been seen to fail**, or only assumed to work? (`val-functional.md`
    §4 owns how that is proven)

---

## 5 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — this installation's criteria | ⭐ the owner of the instance |
| §1, §2, §4 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ lowering a 🔴 to 🟠 locally | **nobody** — ⚠️ log the friction and propose it |

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `dev-backend.md` (⭐ where
authorisation actually lives) · `dev-database.md` · `../owner-2-dev.md` ·
`../owner-3-validation.md` (evidence and result states) · `../imported-patterns.md`.
