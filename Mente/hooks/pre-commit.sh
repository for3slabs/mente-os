#!/usr/bin/env bash
# pre-commit — SHP-LCK-001 · refuses a commit on the base branch.
#
# ⭐ Why a hook and not a paragraph, measured: a rule of exactly this kind
#    existed, written and readable, and was followed ZERO out of fifteen times.
#    ⛔ Declaring a rule is not following it — code 100%, a document 40-60%.
#
# ⚠️ The escape hatch is deliberate: a gate with no way out gets deleted. It is
#    loud, and it leaves a trace that has to be justified.
#
# Install:  ln -sf ../../Mente/hooks/pre-commit.sh .git/hooks/pre-commit
set -u

# ⬜ The base branch is the installation's to name. The engine fixes that there
#    IS one, never what it is called.
BASE="${MENTE_BASE_BRANCH:-}"
if [ -z "$BASE" ]; then
  for candidate in main master trunk; do
    if git show-ref --verify --quiet "refs/heads/$candidate"; then
      BASE="$candidate"
      break
    fi
  done
fi
[ -z "$BASE" ] && exit 0          # ⬜ NOT_MEASURED — no base to protect yet

CURRENT="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || echo '')"
[ -z "$CURRENT" ] && exit 0       # detached head — not a branch commit

if [ "$CURRENT" != "$BASE" ]; then
  exit 0
fi

cat >&2 <<MSG

🔴 REFUSED · commit on the base branch '$BASE'

   SHP-LCK-001 · rules/rule-shipping.md §2

   ⛔ A change enters through a branch and a reviewable proposal — always,
      in every repository, ⚠️ including one where a single person writes.
      A proposal one person opens and reviews alone still leaves the diff
      readable before it enters, which is what it is for.

   ⭐ Measured: this rule existed as a document and was followed 0 of 15 times.
      That is why it is a lock now.

   What to do:
      git switch -c <type>/<scope>      then commit there

   The way out, and it leaves a trace:
      git commit --no-verify            ⚠️ justify it in the block's friction log

MSG
exit 1
