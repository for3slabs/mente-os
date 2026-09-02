#!/usr/bin/env python3
"""probe-declared — does check-declared find a file the piece table omits?

⭐ It is the disk-side check: an undeclared piece produces no error anywhere
else, so nothing but this probe can show it measures at all.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

p = Probe("check-declared", "declare")   # this checker prints paths, not IDs


def plant(rel, body="x\n"):
    q = os.path.join(ROOT, rel)
    d = os.path.dirname(q)
    # track the DIRECTORY when the probe created it, so cleanup removes both
    p.track(d if MARK in os.path.basename(d) else q)
    os.makedirs(d, exist_ok=True)
    open(q, "w", encoding="utf-8").write(body)
    return q


def run_loud():
    """⚠️ This checker prints its finding only WITHOUT --quiet: the harness
    default suppressed the very output the probe reads. A probe whose runner
    hides the answer reports a working check as undetected."""
    import subprocess
    r = subprocess.run([sys.executable, "bin/check-declared"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def verdict(label, setup, expect_in_output=True):
    p.clean()
    setup()
    code, out, err = run_loud()
    seen = MARK in out
    ok = seen == expect_in_output
    print("  %-46s %s %s" % (label, "✅" if ok else "🔴",
                             ("detectado" if seen else "NO DETECTADO")
                             if expect_in_output else
                             ("does NOT fire (correct)" if not seen else "falso positivo")))
    p.clean()
    p.results.append((label, "FAIL" if ok and expect_in_output
                      else "PASS" if ok else "NOT_DETECTED"))
    return ok


print("═══ SABOTAGE · check-declared ═══\n")
p.baseline()

verdict("① un ejecutable sin declarar en bin/",
        lambda: plant("bin/" + MARK + "-tool", "#!/bin/sh\nexit 0\n"))
verdict("② a rule in rules/ with no declared row",
        lambda: plant("rules/" + MARK + "-rule.md", "# x\n"))
verdict("③ un criterio sin declarar en expertise/",
        lambda: plant("memory/principles/expertise/" + MARK + "-x.md", "# x\n"))
verdict("④ a template with no declared row",
        lambda: plant("templates/" + MARK + ".template", "x\n"))

# ⭐ The inverse: a README is skipped on purpose and must not be reported.
# ⛔ It plants a NEW folder, never touching an existing file: a probe whose
# cleanup deletes something real does damage to prove a point.
verdict("⑤ un README nuevo · NO debe reportarse",
        lambda: plant("docs/" + MARK + "-dir/README.md", "# a folder readme\n"),
        expect_in_output=False)

p.crash_guard()
sys.exit(0 if p.report() else 1)
