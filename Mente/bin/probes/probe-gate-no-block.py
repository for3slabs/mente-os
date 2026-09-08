#!/usr/bin/env python3
"""probe-gate-no-block — proves work with no block open is REFUSED.

🔴 THE FAILURE THIS EXISTS FOR, measured 2026-09-06 on a real installation. A
full run researched, built and published real work with no block open, no
boundary declared and nothing written to memory. `bin/status` printed
`⬜ no piece of work open yet`; the assistant read that line out loud to the
owner and carried on. ⛔ Every check was green and the system had held nothing.

⭐ THE ENGINE'S OWN THESIS TURNED ON ITSELF: `pre-edit-standards` already
REPORTED the missing block. Reporting is what a document does. This refuses.

⚠️ AND THE INVERSES OUTNUMBER THE BLOCKS, deliberately (ADR-012): a gate that
obstructs more than it protects is switched off within a week, and then the
cases it was right about are unguarded too.
"""
import os, sys, json, subprocess, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                              # noqa: E402

HOOK = os.path.join(ROOT, "hooks", "gate-no-block.py")
ACTIVE = os.path.join(ROOT, "work", "blocks", "active")
results = []


def case(label, ok, detail=""):
    results.append((label, ok))
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))


def fire(path, env=None):
    e = dict(os.environ)
    e.pop("MENTE_SCRATCH", None)
    if env:
        e.update(env)
    r = subprocess.run([sys.executable, HOOK], input=json.dumps(
        {"tool_input": {"file_path": path}}), capture_output=True,
        text=True, timeout=30, env=e)
    return r


_out = os.path.join(tempfile.gettempdir(), "probe-gnb-work.md")
_open = bool(__import__("glob").glob(os.path.join(ACTIVE, "*", "BLOCK.md")))

# ── ① THE REFUSAL · the case the whole file exists for ─────────────────────
if not _open:
    r = fire(_out)
    case("① 🔴 ⭐ work with NO block open is REFUSED",
         r.returncode == 2, "exit=%d" % r.returncode)
    # ⛔ A refusal that does not say what to do next is a wall. Measured
    # elsewhere in this engine: a refusal naming its own bypass is a suggestion,
    # and one naming nothing is a person stuck.
    _said = (r.stdout + r.stderr).lower()
    case("①b ⭐ and it names how to open one",
         "new-block" in _said and "boundary" in _said)
    case("①c ⭐ and it offers a way out for a throwaway",
         "mente_scratch" in _said)
else:
    # ⬜ CHK-CAU-003 · said out loud, never swallowed.
    print("  ⬜ ①-①c NOT MEASURED · a block is already open in this tree")

# ── ② THE INVERSES · everything a gate must NOT block ──────────────────────
r = fire(_out, {"MENTE_SCRATCH": "1"})
case("② a declared throwaway passes", r.returncode == 0,
     "exit=%d" % r.returncode)
r = fire(os.path.join(ROOT, "docs", "anything.md"))
case("②b the engine's own folder passes — installing needs no block",
     r.returncode == 0, "exit=%d" % r.returncode)
r = fire("")
case("②c an action naming no file passes", r.returncode == 0,
     "exit=%d" % r.returncode)

# ── ③ IT NEVER FAILS CLOSED ON ITS OWN BUG ─────────────────────────────────
# 🔴 A gate that refuses because IT crashed locks the person out of their own
# machine. ⚠️ Three malformed payloads: not JSON, JSON that is not an object,
# and an object with no tool_input.
for _sfx, (_label, _payload) in zip(("", "b", "c"),
                                    (("not JSON", "}{"), ("a list", "[]"),
                                     ("no tool_input", '{"x":1}'))):
    e = dict(os.environ); e.pop("MENTE_SCRATCH", None)
    r = subprocess.run([sys.executable, HOOK], input=_payload,
                       capture_output=True, text=True, timeout=30, env=e)
    # ⚠️ One label per case, even inside a loop — the battery refuses a
    # repeat, and a duplicated label hides whichever of them failed.
    case("③%s %-21s → allowed, never a trace" % (_sfx, _label),
         r.returncode == 0 and "Traceback" not in (r.stdout + r.stderr),
         "exit=%d" % r.returncode)

# ── ④ WITH A BLOCK OPEN IT GETS OUT OF THE WAY ─────────────────────────────
# ⭐ Measured against a REAL block created by the engine's own command — ⛔ not
# a folder this probe faked, which would measure the fixture.
# ⚠️ The block is placed directly, not through `bin/new-block`: on an
# un-instantiated engine that command refuses (no owner declared, correctly),
# and a case that cannot run is a case that measures nothing — found here.
# ⭐ What this asserts is the gate's own question — "does a BLOCK.md exist under
# active/" — so the fixture only has to satisfy that, not the block contract.
_made = None
if not _open:
    _made = os.path.join(ACTIVE, "probe-gnb")
    try:
        os.makedirs(_made, exist_ok=True)
        open(os.path.join(_made, "BLOCK.md"), "w",
             encoding="utf-8", newline="").write("# BLOCK · probe-gnb\n")
    except OSError:
        _made = None
try:
    if _made and os.path.isdir(_made):
        r = fire(_out)
        case("④ 🔴 ⭐ with a block open, the same write passes",
             r.returncode == 0, "exit=%d" % r.returncode)
    else:
        print("  ⬜ ④ NOT MEASURED · could not open a block to test against")
finally:
    if _made and os.path.isdir(_made):
        plat.rmtree(_made)

# ── ⑤ IT IS WIRED, not merely present ──────────────────────────────────────
# 🔴 The measured failure was never a missing gate: it was a gate nothing
# called. ⛔ A hook on disk that no settings file names protects nothing.
_tpl = os.path.join(ROOT, "templates", "claude-settings.json.template")
_txt = open(_tpl, encoding="utf-8").read() if os.path.isfile(_tpl) else ""
case("⑤ 🔴 ⭐ the settings template actually calls it",
     "gate-no-block.py" in _txt)
case("⑤b ⛔ and on the tools that write",
     '"matcher": "Edit|Write|MultiEdit"' in _txt)

# ── ⑦ 🔴 A BLOCK IS OPEN, BUT THIS PATH IS OUTSIDE IT ──────────────────────
# 🔴 THE FAILURE, measured 2026-09-07. A run opened a block correctly and then
# wrote its deliverable to the repository ROOT — outside everything §B named.
# `check-block` reported 0 violations and `check-document` audited 58 documents
# without ever seeing the file. ⛔ The gate refused work with NO block and waved
# through work OUTSIDE the block: the same hole, one step along.
_sc = os.path.join(ACTIVE, "probe-gnb-scope")
_made2 = None
if not _open:
    try:
        os.makedirs(_sc, exist_ok=True)
        open(os.path.join(_sc, "BLOCK.md"), "w", encoding="utf-8",
             newline="").write(
            "# BLOCK · probe-gnb-scope\n\n## B · Scope\n\n### ✅ IN\n"
            "- `Mente/Cerebro/probe-scope/` — the material\n\n"
            "### ⛔ OUT\n- nothing\n")
        _made2 = _sc
    except OSError:
        _made2 = None
try:
    if _made2:
        r = fire(os.path.join(ROOT, "Cerebro", "probe-scope", "x.md"))
        case("⑦ ⭐ a path INSIDE §B passes", r.returncode == 0,
             "exit=%d" % r.returncode)
        r = fire(os.path.join(os.path.dirname(ROOT), "LOOSE.md"))
        case("⑦b 🔴 ⭐ a path OUTSIDE every §B is REFUSED",
             r.returncode == 2, "exit=%d" % r.returncode)
        _said = (r.stdout + r.stderr).lower()
        # ⛔ And the refusal must name the dishonest way out, because that is
        # the one an assistant reaches for: widen §B to fit what it planned.
        case("⑦c ⛔ and it refuses silent widening of the scope",
             "do not widen the scope silently" in _said)
    else:
        # ⬜ CHK-CAU-003 · said out loud, never swallowed.
        print("  ⬜ ⑦-⑦c NOT MEASURED · could not place a scoped block")
finally:
    if _made2 and os.path.isdir(_made2):
        plat.rmtree(_made2)

# ── ⑥ IT LEAVES NOTHING BEHIND ─────────────────────────────────────────────
# 🔴 Measured 2026-09-06, and it reached main: `beat(mente, name)` takes the
# Mente ROOT first, and this gate passed its own label there — so every call
# wrote into a folder named after the gate, BESIDE the repository. Three stray
# files were committed before anyone looked. ⛔ A hook that litters outside the
# folder breaks the one promise the engine makes: delete it and it is gone.
_stray = os.path.join(os.path.dirname(ROOT), "gate-no-block")
case("⑥ 🔴 ⭐ the gate writes its beat inside Mente/, not beside it",
     not os.path.exists(_stray),
     "🔴 %s exists" % _stray if os.path.exists(_stray) else "clean")
# ⭐ And the positive half: it DOES leave a beat, where check-gates reads it.
# ⛔ Without this, "writes nothing anywhere" would also pass.
case("⑥b ⭐ and the beat is where check-gates looks for it",
     os.path.isfile(os.path.join(ROOT, ".beats", "gate-no-block")))

# ── ⑨ 🔴 BASH IS A DOOR TOO, AND IT WAS THE ONLY ONE BEING USED ────────────
# 🔴 THE FAILURE, measured 2026-09-07 on a real Windows run. A whole project was
# built and shipped — nine files — and NOT ONE gate fired. The gates were wired,
# alive, and left beats when called by hand. ⛔ The assistant simply never used
# the door they watched: it wrote every file with `cat > path <<'EOF'` from
# Bash, while the write gates sat on `Edit|Write|MultiEdit`. The transcript
# counted **Bash 83 uses · Write/Edit 0**.
# ⭐ Wiring is not coverage. A gate watching a door nobody walks through reports
# green forever, and every check above it stays green with it.
def fire_cmd(command, env=None):
    e = dict(os.environ)
    e.pop("MENTE_SCRATCH", None)
    if env:
        e.update(env)
    return subprocess.run([sys.executable, HOOK], input=json.dumps(
        {"tool_input": {"command": command}}), capture_output=True,
        text=True, timeout=30, env=e)


_cmd_out = os.path.join(tempfile.gettempdir(), "probe-gnb-bash.md")
if not _open:
    r = fire_cmd("cat > %s <<'EOF'\nhola\nEOF" % _cmd_out)
    case("⑨ 🔴 ⭐ a `cat >` from Bash is REFUSED, exactly as a Write is",
         r.returncode == 2, "exit=%d" % r.returncode)
    r = fire_cmd("echo hi > %s" % _cmd_out)
    case("⑨b 🔴 a redirection is a write whatever the verb", r.returncode == 2,
         "exit=%d" % r.returncode)
else:
    # ⬜ CHK-CAU-003 · said out loud. A block is open in THIS tree, so the
    # no-block refusal cannot be measured — and a case that cannot run reports
    # NOT MEASURED, never a green it did not earn.
    print("  ⬜ ⑨ NOT MEASURED · a block is open in this tree")
    _src = open(HOOK, encoding="utf-8").read()
    case("⑨ 🔴 ⭐ the gate reads a Bash command's writes",
         "cmd_writes" in _src and "tool_input" in _src)

# ⛔ AND THE HALF THAT DECIDES WHETHER IT SURVIVES: ordinary tooling must pass.
# 🔴 A gate that refuses `npm install` is switched off within a day (ADR-012),
# and then nothing is governed at all.
_tooling = [(_c, fire_cmd(_c).returncode)
            for _c in ("npm install", "git commit -m x", "ls -la && grep x f")]
_refused = ["%s→%d" % (c, rc) for c, rc in _tooling if rc != 0]
case("⑨c ⛔ ordinary tooling is NEVER refused (npm · git · a read)",
     not _refused, ", ".join(_refused) or "3 of 3 allowed")

# ⬜ AND AN UNRECOGNISED COMMAND IS NOT MEASURED, never a refusal.
r = fire_cmd("herramienta-que-nadie-conoce x")
case("⑨d ⬜ an unrecognised command is allowed and SAID, not refused",
     r.returncode == 0 and "NOT MEASURED" in r.stderr, "exit=%d" % r.returncode)

# ── ⑩ 🔴 AND THE WIRING MUST NAME BASH, or every case above is theatre ─────
# ⭐ The gate can be perfect and still never run. This reads the shipped
# template, because that is what lands in somebody's installation.
_tpl = os.path.join(ROOT, "templates", "claude-settings.json.template")
try:
    _cfg = json.load(open(_tpl, encoding="utf-8"))
    _m = [e.get("matcher", "") for e in _cfg.get("hooks", {}).get(
        "PreToolUse", []) for h in e.get("hooks", [])
        if "gate-no-block" in h.get("command", "")]
    case("⑩ 🔴 ⭐ the shipped wiring puts this gate on Bash too",
         any("Bash" in m for m in _m), " · ".join(_m) or "not wired at all")
except (OSError, ValueError) as _e:
    print("  ⬜ ⑩ NOT MEASURED · %s" % type(_e).__name__)

print("\n  ⬜ NOT MEASURED · whether an assistant OBEYS the refusal · that runs\n"
      "     outside this engine · these cases prove the refusal happens")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: none")
sys.exit(0 if good == len(results) else 1)
