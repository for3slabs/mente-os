#!/usr/bin/env python3
"""probe-checks — does check-checks detect what rule-checks-must-measure.md claims?

⭐ The validator that audits the validators. Its own probe is the one that
must be hardest to fool.
"""
import os, sys
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
p.crash_guard()

sys.exit(0 if p.report() else 1)
