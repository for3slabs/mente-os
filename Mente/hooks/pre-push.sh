#!/usr/bin/env bash
# pre-push — LAYER 2 of the accounts gate: the one that cannot be walked around.
#
# ⭐ WHY IT EXISTS, measured. `hooks/gate-accounts.py` reads the TEXT of a
# command, so not writing the verb literally is enough to pass it. Seven ways of
# writing the same push were tested and FIVE got through: an alias, a shell
# function, a variable holding the verb, an `eval`, and an argument-builder. The
# recorded debt said "an alias"; the reality was five.
#
# ⛔ THE LESSON GENERALISES: a pattern over command text NEVER covers every way
# of invoking a command. It does not matter how many patterns are added — there
# is always one more. A defence that lives only there is a defence with a
# schedule.
#
# ⭐ THIS ONE IS RUN BY GIT, during the real push, with the remote already
# resolved. There is no text to interpret — there is a destination to verify.
# However the command was written, it arrives here.
#
#   layer 1  gate-accounts.py   fast, explains BEFORE, and can be walked around
#   layer 2  THIS ONE           cannot be walked around, but speaks only at push
#
# ⬜ Installation: link it into .git/hooks/pre-push. Until it is linked, layer 1
#    is the only defence — and layer 1 can be avoided.
#
# Exit: 0 lets the push through · 1 ABORTS it.
set -uo pipefail

REMOTE_NAME="${1:-}"
REMOTE_URL="${2:-}"

# ⚠️ THIS FILE IS INVOKED FROM .git/hooks/pre-push, normally through a symlink,
# so BASH_SOURCE resolves to .git/hooks/ and not to the engine. ⛔ Measured
# elsewhere: the hook ran, reported "no registry" over a registry with rows, and
# let EVERYTHING through in silence.
# 🔴 A guard that fails OPEN is worse than no guard: it gives confidence without
# giving protection. The root is asked of git, which always knows it, with the
# resolved symlink as the fallback.
# ⚠️ Reading the host's tool is bounded by ADR-031: read only, never over the
# network, and its absence is a gap rather than a failure.
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$ROOT" ]; then
  SELF="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}")"
  ROOT="$(cd "$(dirname "$SELF")/../.." && pwd)"
fi
# ⬜ An explicitly declared registry is used AS DECLARED — ⛔ never quietly
# replaced by a discovered one. A fallback that overrides a declaration makes
# the hook verify against a file the operator did not choose, and the operator
# has no way to tell. Discovery applies only when nothing was declared.
if [ -n "${MENTE_ACCOUNTS:-}" ]; then
  REG="$MENTE_ACCOUNTS"
else
  REG="$ROOT/Mente/accounts.tsv"
  [ -f "$REG" ] || REG="$ROOT/accounts.tsv"
fi

# ⬜ No registry means nothing to verify against. A fresh clone has none on
# purpose, and aborting there would block anyone's first push. Says so and lets
# it through — ⚠️ never silently, or "unverified" reads as "verified".
if [ ! -f "$REG" ]; then
  echo "⬜ pre-push: no accounts registry — this destination was NOT verified" >&2
  exit 0
fi

# ⭐ The destination is matched against what the registry DECLARES, never parsed
# out of the URL. ⛔ Parsing means knowing every host's address shape, and the
# one not covered passes silently. The registry already holds the names.
REPO=""
while IFS=$'\t' read -r repo cuenta rol remoto ruta why guia; do
  case "$repo" in ''|'#'*|repo) continue ;; esac
  # ⚠️ Matched case-insensitively: a host that treats names case-insensitively
  # would otherwise let a differently-cased spelling walk straight past.
  if printf '%s' "$REMOTE_URL" | grep -qiF -- "$repo"; then
    REPO="$repo"; ROL="$rol"
    break
  fi
done < "$REG"

if [ -z "$REPO" ]; then
  # 🔴 ACC-LYR-003 · FAIL CLOSED. There is no "ask" inside a push: it either proceeds or it
  # aborts. ⭐ Aborting costs nothing — the work stays local. Letting an
  # unverified destination through costs everything, invisibly: it succeeds.
  cat >&2 <<MSG

🔴 PUSH ABORTED — this destination is not declared

   ⛔ An undeclared repository has no owner, no stated reason to exist and no
   access guide. If the work leaves, nobody knows where it went.

   ⭐ This is the layer that cannot be walked around: git runs it during the
      real push, so an alias, a function, an \`eval\` or a built argument list
      all arrive here.

   The way out:
     1. add its row to the accounts registry — with its reason to exist
     2. Mente/bin/check-accounts
     3. push again

   ⚠️ Your work is still local. Nothing was lost.

MSG
  exit 1
fi

# 🔴 CHECKED BEFORE anything else, and that order IS the rule. A retired
# repository IS registered — it stays declared on purpose, because one that
# disappears from the table becomes invisible again and the reason it was
# retired disappears with it. ⛔ A gate that asks "registered?" first answers
# YES and lets the push through.
if [ "${ROL:-}" = "archivado" ]; then
  cat >&2 <<MSG

🔴 PUSH ABORTED — \`$REPO\` is RETIRED

   A retired repository is kept for reading, never for writing. Pushing there
   leaves the work somewhere the system already declared dead, and nobody is
   going to look for it.

   ⭐ This is the layer that cannot be walked around.

   ⚠️ Your work is still local. Push to the repository that succeeded this one.

MSG
  exit 1
fi

exit 0
