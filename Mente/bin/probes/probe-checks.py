#!/usr/bin/env python3
"""probe-checks — does check-checks detect what rule-checks-must-measure.md claims?

⭐ The validator that audits the validators. Its own probe is the one that
must be hardest to fool.
"""
import ast, glob, os, sys
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

BIN = os.path.join(ROOT, "bin")
p = Probe("check-checks", "CHK")


def plant(body, shebang="#!/usr/bin/env python3"):
    q = p.track(os.path.join(BIN, MARK + "-checker"))
    open(q, "w", encoding="utf-8").write(shebang + "\n" + body)
    os.chmod(q, 0o755)
    return q


print("═══ SABOTAGE · check-checks ═══\n")
p.baseline()

p.case("① A · a loose comparison of an id",
       lambda: plant('text = "abc"\nsid = "dc733bc1"\nif sid in text:\n    pass\n'),
       "CHK-CMP-001")
p.case("② A · a loose comparison of a hash",
       lambda: plant('text = ""\ncommit_hash = "016"\nif commit_hash not in text:\n'
                     '    pass\n'), "CHK-CMP-001")
p.case("③ C · an exit status clobbered by a substitution",
       lambda: plant('echo "$(build_label)" "$?"\n', "#!/bin/bash"), "CHK-CLB-001")
p.case("④ D · requires a path the repo excludes",
       lambda: plant('import os\nos.path.exists("secrets")\n'), "CHK-TRV-001")
p.case("⑤ D-bis · an unguarded open() of a declared path",
       lambda: plant('CFG = "some/config.json"\n'
                     'text = open(CFG, encoding="utf-8").read()\n'), "CHK-TRV-002")
p.case("⑥ CAU · an entry point with no exception guard",
       lambda: plant('import sys\n\n\ndef main():\n    return 0\n\n\n'
                     'if __name__ == "__main__":\n    sys.exit(main())\n'),
       "CHK-CAU-002")

p.case("⑥b IND · a bare ✅ that never says what it measured",
       lambda: plant('import sys\n\n\ndef main():\n'
                     '    print("✅ everything is fine")\n    return 0\n\n\n'
                     'if __name__ == "__main__":\n'
                     '    try:\n        sys.exit(main())\n'
                     '    except Exception as e:\n        print(e)\n'
                     '        sys.exit(1)\n'),
       "CHK-IND-002")

p.case("⑥c CAU · a guard that swallows the object in silence",
       lambda: plant('import os, sys\n\n\ndef main():\n'
                     '    for f in os.listdir("."):\n'
                     '        try:\n'
                     '            open(f, encoding="utf-8").read()\n'
                     '        except OSError:\n'
                     '            continue\n'
                     '    print("✅ %d checked" % 1)\n    return 0\n\n\n'
                     'if __name__ == "__main__":\n'
                     '    try:\n        sys.exit(main())\n'
                     '    except Exception as e:\n        print(e)\n'
                     '        sys.exit(1)\n'),
       "CHK-CAU-003")

# ⭐ the inverse of ⑥c: the SAME guard, with its skip declared, must not fire.
p.inverse("⑥d CAU · the same guard, with its skip declared",
          lambda: plant('import os, sys\n\n\ndef main():\n'
                        '    for f in os.listdir("."):\n'
                        '        try:\n'
                        '            open(f, encoding="utf-8").read()\n'
                        '        except OSError:\n'
                        '            continue  # ⬜ unreadable, skipped · counted below\n'
                        '    print("✅ %d checked" % 1)\n    return 0\n\n\n'
                        'if __name__ == "__main__":\n'
                        '    try:\n        sys.exit(main())\n'
                        '    except Exception as e:\n        print(e)\n'
                        '        sys.exit(1)\n'))

p.inverse("⑦ a CORRECT validator",
          lambda: plant('import os, sys\n\n\ndef main():\n'
                        '    P = "some/config.json"\n'
                        '    if os.path.exists(P):\n'
                        '        open(P, encoding="utf-8").read()\n'
                        '    return 0\n\n\n'
                        'if __name__ == "__main__":\n'
                        '    try:\n        sys.exit(main())\n'
                        '    except Exception as e:\n'
                        '        print(e)\n        sys.exit(1)\n'))
# ── CHK-XIT-001 · the exit code carries the verdict ────────────────────────
# ⛔ A hook, a gate and the battery all decide on the NUMBER, not the text. A
# validator returning the same code for "this is wrong" and "I could not
# measure" makes those indistinguishable to every caller — ⭐ and they are
# opposite problems: REJECT does not proceed, PENDING is a gap to be filed.
# ⚠️ The entry point catches its exceptions, because CHK-CAU-002 demands it:
# a fixture missing that fires the WRONG rule, and an inverse case then reports
# a false positive against a check it was not testing.
_OK = ('import sys\n\n\ndef main():\n    return %s\n\n\n'
       'if __name__ == "__main__":\n    try:\n        sys.exit(main())\n'
       '    except Exception as e:\n        print(e)\n        sys.exit(1)\n')

p.case("⑧ ⛔ a code the contract does not declare",
       lambda: plant(_OK % "7"), "CHK-XIT-001")

# ⭐ Each declared code is accepted — including 2, which twelve validators use
# for "I could NOT measure" and which must never read as a failure.
for _c, _what in (("0", "PASS"), ("1", "REJECT"), ("2", "PENDING"), ("3", "WARN")):
    p.inverse("⑧%s ⭐ exit %s (%s) is declared → accepted"
              % ("abcd"["0123".index(_c)], _c, _what),
              lambda c=_c: plant(_OK % c))

# ── ⑨ 🔴 A PROBE MUST NOT LEAVE THE TREE DIRTIER THAN IT FOUND IT ──────────
# 🔴 THE FAILURE, measured 2026-09-07 on a real Windows install. Six probes
# sabotage a real engine file and restore it through a plain
# `open(..., "w", encoding="utf-8")`. On Windows that turns every "\n" into
# "\r\n": `probe-grade` left `rules/contract-quality-verdict.md` with 311 CRLF
# lines where it had found 311 LF ones. ⛔ Then `probe-init ㉘` — whose whole
# job is "nothing carries CRLF" — reported the mess its own neighbour had just
# made. 3 of the 10 failures the battery showed were probes contaminating each
# other, and the owner was told they were defects.
# ⚠️ The same bug this engine documents fixing in `bin/init`, never fixed in
# the probes that check it.
# ⚠️ Only names that point at a SHIPPED engine file. 🔴 `FIX`/`LOCAL` were
# in this list at first and the case fired on `probe-config`, whose
# fixtures live under a MARK-prefixed temp folder and are thrown away —
# a rule that flags correct behaviour is one somebody switches off.
_REAL = ("CONTRACT", "RULE", "_rule", "_idx", "_pr")
_unsafe = []
for _p in sorted(glob.glob(os.path.join(ROOT, "bin", "probes", "probe-*.py"))):
    try:
        _tree = ast.parse(open(_p, encoding="utf-8").read())
    except (OSError, SyntaxError):
        # ⬜ CHK-CAU-003 · said out loud, never swallowed.
        _unsafe.append("⬜ unparsed:" + os.path.basename(_p))
        continue
    for _n in ast.walk(_tree):
        if not (isinstance(_n, ast.Call)
                and getattr(_n.func, "id", "") == "open"):
            continue
        _m = next((a.value for a in _n.args[1:]
                   if isinstance(a, ast.Constant)), "r")
        if ("w" not in str(_m) and "a" not in str(_m)) or \
                any(k.arg == "newline" for k in _n.keywords):
            continue
        # ⭐ Only writes aimed at the REAL tree matter: a probe's own temp
        # fixture is thrown away, and demanding `newline=""` there would be
        # noise that gets the rule switched off.
        _t = _n.args[0] if _n.args else None
        if (getattr(_t, "id", "") or getattr(_t, "attr", "")) in _REAL:
            _unsafe.append("%s:%d" % (os.path.basename(_p), _n.lineno))
_ok9 = not _unsafe
print("  %-58s %s %s" % ("⑨ 🔴 ⭐ no probe rewrites a real file with translation on",
                         "✅" if _ok9 else "🔴",
                         ", ".join(_unsafe)[:44] or "clean"))
p.results.append(("⑨ probes no traducen", "PASS" if _ok9 else "DIRTY"))


p.crash_guard()

sys.exit(0 if p.report() else 1)
