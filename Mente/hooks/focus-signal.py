#!/usr/bin/env python3
"""focus-signal · UserPromptSubmit — the block the owner just asked for becomes the FOCUS.

⭐ The owner, 2026-10-03: *"tu fuente de verificación es lo que te pedí que hicieras recientemente
… al menos que te diga 'vamos a cambiar de tema a mak-tub', ok, son otras skills"*.

The focus decides which ON-DEMAND skills are exposed (`bin/connection focus`): only the ones the
block — or its campaign — declares. This hook reads each request and moves the focus when the
request NAMES a block, so the skills follow the work without anyone typing a command.

When does a request name a block — exactly, never by a guess:
  · its full hyphenated name anywhere (`pilares-documentos`, `mak-tub`) → that block
  · a change-of-topic phrase ("vamos a trabajar en…", "cambiemos de tema a…", "pasemos a…")
    followed, within a few words, by words that match ONE block's name → that block
    ("panel de administración" → panel-administrador-global: `panel` + `administr…`)
  · ties break on evidence, in this order: more words matched · the word CLOSEST to the
    change-of-topic phrase ("pasemos a pilares, ya contestó la clienta" → pilares, not
    control-clientes) · an ACTIVE block over a blocked one (the panel being worked, not the
    one waiting)
  · still equal → it says so and moves NOTHING: a wrong focus switches the wrong
    skills on, and the cost of asking is one line

⚠️ An exposed skill is seen from the NEXT session or after `/reload-skills` (measured
2026-09-26) — when a switch changes what is linked, this hook says so, every time.

⛔ NEVER BLOCKS AND NEVER RAISES. Silent when nothing moves: zero tokens on most requests.
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(MENTE, "bin"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TRIGGER = re.compile(
    r"\b(vamos a (trabajar|seguir|continuar|pasar|regresar|volver|meternos|enfocarnos)"
    r"|cambi\w* (de tema|a)|pasemos|trabajemos|sigamos|retomemos|regresemos|volvamos"
    r"|enfoquemonos|enfocate|ahora (con|en|vamos)|nos vamos a)\b")
WINDOW = 8          # words after the trigger that may name the block
STEM = 6            # `administracion` and `administrador` share `admini`


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


ACTIVE = set()


def blocks():
    out = []
    for st in ("active", "blocked"):
        d = os.path.join(MENTE, "work", "blocks", st)
        if os.path.isdir(d):
            here = [b for b in sorted(os.listdir(d))
                    if os.path.isfile(os.path.join(d, b, "BLOCK.md"))]
            if st == "active":
                ACTIVE.update(here)
            out += here
    return out


def _hit(token, words):
    """→ index of the first word that matches the token, or None."""
    for i, w in enumerate(words):
        if (w == token) if len(token) < STEM else (len(w) >= STEM and w[:STEM] == token[:STEM]):
            return i
    return None


def resolve(prompt, names):
    """→ (block, why) · (None, why-ambiguous) · (None, None) when the request names no block."""
    text = norm(prompt)
    full = [b for b in names if "-" in b and re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(b), text)]
    if len(full) == 1:
        return full[0], "named `%s`" % full[0]
    if len(full) > 1:
        return None, "names %s" % ", ".join(full)
    m = TRIGGER.search(text)
    if not m:
        return None, None
    words = re.findall(r"[a-z0-9]+", text[m.end():])[:WINDOW]
    scored = []
    for b in names:
        toks = [t for t in b.split("-") if t]
        at = {t: _hit(t, words) for t in toks}
        hits = [t for t in toks if at[t] is not None]
        if not hits:
            continue
        unique = any(len(t) >= STEM and not any(t in o.split("-") for o in names if o != b)
                     for t in hits)
        if len(hits) == len(toks) or len(hits) >= 2 or unique:
            scored.append((len(hits), -min(at[t] for t in hits), b in ACTIVE, b))
    if not scored:
        return None, None
    scored.sort(reverse=True)
    if len(scored) > 1 and scored[0][:3] == scored[1][:3]:
        return None, "could be %s or %s" % (scored[0][3], scored[1][3])
    return scored[0][3], "«%s» → `%s`" % (" ".join(words[:5]), scored[0][3])


def main():
    try:
        from _beat import beat, paused
        beat(MENTE, "focus-signal")
        if paused(MENTE):
            return 0
    except Exception:                                          # noqa: BLE001
        pass
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0
    if not isinstance(payload, dict):
        return 0
    prompt = payload.get("prompt") or ""
    if not isinstance(prompt, str) or not prompt.strip():
        return 0
    import connection_lib as C
    block, why = resolve(prompt, blocks())
    if not block:
        if why:
            print("🎯 FOCUS unchanged — your message %s · `bin/connection focus <block>` if "
                  "the topic changes" % why)
        return 0
    if C.read_focus().get("block") == block:
        return 0                                   # already there: nothing to say
    r = subprocess.run([sys.executable, os.path.join(MENTE, "bin", "connection"), "focus",
                        block, "--by", "prompt"], capture_output=True, text=True, timeout=30)
    out = (r.stdout + r.stderr).strip()
    on = re.search(r"🟢 on : (.*)", out)
    off = re.search(r"⚪ off: (.*)", out)
    msg = "🎯 FOCUS → `%s` (%s) · skills on: %s · off: %s" % (
        block, why, on.group(1) if on else "?", off.group(1) if off else "?")
    if "switched on or off" in out:
        msg += " · ⚠️ what is exposed changed: ask the owner to run /reload-skills"
    if r.returncode:
        msg = "🎯 FOCUS → `%s` failed: %s" % (block, out.splitlines()[-1] if out else r.returncode)
    print(msg)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:                                     # noqa: BLE001
        print("⚠️  focus-signal.py · %s: %s" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(0)
