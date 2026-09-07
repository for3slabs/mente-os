#!/usr/bin/env bash
# session-start — the system reports its own state without being asked.
#
# Implements ADR-024 · the audit runs by itself; asking for it means it is not
# automated. The reasoning, the evidence and what would retire this decision
# live in that record — ⛔ not here. A hook is not a diary.
#
# Two constraints this file exists to obey, both stated in hooks/README:
#   1 · NEVER block the session. Failing must not stop the work.
#   2 · Speak ONLY when something is wrong. Silence is the healthy output.
set -uo pipefail
MENTE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ── ⬜ WHAT RUNS AT STARTUP IS THE INSTALLATION'S ────────────────────────────
# MENTE_STARTUP_CHECKS: space-separated validator names. Unset means DISCOVER
# every `check-*` in bin/ — ⭐ so adding a validator does not mean editing this
# hook. ⛔ Naming them here would make this file grow with every new check,
# which is the shape that turns a hook into a list nobody maintains.
read -ra CHECKS <<< "${MENTE_STARTUP_CHECKS:-}"
if [ "${#CHECKS[@]}" -eq 0 ]; then
  for c in "$MENTE"/bin/check-*; do
    [ -x "$c" ] || continue
    n="$(basename "$c")"
    # ⛔ NOT EVERY VALIDATOR BELONGS AT STARTUP. `check-clear-ready` answers
    # "would a cut lose anything" — and mid-session the honest answer is YES,
    # because work in progress is uncommitted BY DEFINITION. ⚠️ Running it here
    # reports normal working state as a fault every single launch, and a hook
    # that cries wolf at startup is the first one anybody disables.
    # ⭐ It is asked BEFORE a cut, which is the only moment its answer changes
    # anything.
    [ "$n" = "check-clear-ready" ] && continue
    CHECKS+=("$n")
  done
fi

# ── ⏸️ THE PAUSE SWITCH · honoured HERE, not announced elsewhere ────────────
# 🔴 Measured 2026-09-06: the owner could not tell whether the system was
# running, and had no way to stop it. ⛔ A switch the gates do not read is a
# label, not a switch — so every gate checks the same file, and `bin/off`
# only writes it.
# ⚠️ Silent on purpose: a pause the owner asked for is not a finding.
[ -f "$MENTE/.off" ] && exit 0

# ── THE HEARTBEAT · written FIRST, before anything can fail ──────────────────
# ⛔ This hook is silent when all is well — and equally silent if it is dead.
# ⭐ Healthy silence and dead silence are indistinguishable from the inside, but
# a stamp makes them distinguishable AFTERWARDS: "it said nothing" becomes "it
# has said nothing since <date>".
# ⚠️ LOCAL, not `date -u`. Every reader of this stamp compares it against the
# local date; writing UTC here made the two halves of one subtraction use two
# clocks, and the gap read one day too old west of UTC.
date +%Y-%m-%d > "$MENTE/.heartbeat" 2>/dev/null || true

# ── WHICH SESSION IS THIS ────────────────────────────────────────────────────
# ⬜ The host may hand a session id on stdin. Read it if present, and say so if
# not: ⛔ guessing which session is current produces alarms about a transcript
# nobody is writing to. A validator run by hand falls back to its own default
# and knows that it did.
payload="$(timeout 2 cat 2>/dev/null || true)"
MENTE_SESSION_ID="$(printf '%s' "$payload" \
  | grep -o '"session_id"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | head -1 | sed 's/.*"\([^"]*\)"$/\1/')"
export MENTE_SESSION_ID

# ── THE AUDIT · one loop, no per-validator branches ──────────────────────────
# ⭐ Every validator obeys the same contract: 0 clean · non-zero has findings ·
# `--quiet` is the EXIT CODE ONLY — CHK-QUI-001. ⛔ Because the contract is
# uniform, this needs no knowledge of what any of them checks — that is what
# makes it scale.
#
# ⚠️ TWO CALLS, AND THAT IS THE CONTRACT, NOT WASTE. `--quiet` answers "is
# anything wrong" for every validator; only the few that say yes are asked
# again for the reason. 🔴 Reading output from a `--quiet` run was a third
# reading of the same flag — a hook wanted silence, a probe wanted the cause,
# and this wanted both — and each consumer had quietly invented its own.
found=0
for name in "${CHECKS[@]}"; do
  bin="$MENTE/bin/$name"
  [ -x "$bin" ] || continue          # ⬜ declared but absent · skipped, counted below
  "$bin" --quiet >/dev/null 2>&1 || {
    printf '⚠️  %s\n' "$name"
    "$bin" 2>/dev/null | grep -E '🔴|🟡|⬜' | head -4
    found=$((found + 1))
  }
done

# ── 🔴 SAY WHERE THE WORK STANDS · the hook's other job ─────────────────────
# 🔴 Measured 2026-09-07. This hook ran validators and stayed silent when they
# were clean — so the one moment the system could orient the assistant, it said
# nothing. ⛔ The assistant reached turn one never told to read RESUME or check
# for an open block, and worked as if the system were not there. The owner:
# "it is installed, it uses it now and then, but it has not read how to behave."
# ⚠️ This is NOT the "speak only on 🔴" rule broken: that rule is about
# FINDINGS. Where the work stands is not a finding — it is the brief, and a
# brief withheld is what the whole engine exists to prevent.
# ⭐ Two lines, and only what changes the first move.
_open=0
for _b in "$MENTE"/work/blocks/active/*/BLOCK.md; do
  [ -f "$_b" ] && _open=$((_open + 1))
done
if [ "$_open" -gt 0 ]; then
  printf '📦 %d piece(s) of work open · read its §A-E and stay inside its §B\n' "$_open"
else
  printf '⬜ no piece of work open · ⛔ nothing may be written until one is\n'
fi
# ⚠️ Named, never pasted: a brief the hook prints is a brief nobody re-reads.
[ -f "$MENTE/memory/RESUME.md" ] && \
  printf '🧭 read Mente/memory/RESUME.md first — where we left off\n'

[ "$found" -gt 0 ] && printf '\n👉 run: Mente/bin/probes/run-all.py\n'

exit 0   # ⛔ always 0 — this hook informs, it never blocks
