#!/usr/bin/env python3
"""probe-shipping — does check-shipping detect what rule-shipping.md claims?

⭐ And it INVOKES the gate rather than checking it exists: presence is not
compliance, and a gate nobody has seen refuse is a gate nobody has tested
(rule-checks-must-measure.md §2).
"""
import os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

RULE = os.path.join(ROOT, "rules", "rule-shipping.md")
HOOK = os.path.join(ROOT, "hooks", "pre-commit.sh")
ORIG = open(RULE, encoding="utf-8").read()

p = Probe("check-shipping", "SHP", also=("rule-shipping.md",))
_clean = p.clean


def clean():
    """⭐ Restore what this probe EDITS, not only what it creates."""
    open(RULE, "w", encoding="utf-8").write(ORIG)
    _clean()


p.clean = clean


def edit(a, b):
    s = open(RULE, encoding="utf-8").read()
    open(RULE, "w", encoding="utf-8").write(s.replace(a, b))


print("═══ A · SABOTAJE · check-shipping ═══\n")
p.baseline()

p.case("① una etapa del ciclo sin dueño",
       lambda: edit("| 10 | ⭐ **DETECT the merge** — look, do not ask | §8 |",
                    "| 10 | ⭐ **DETECT the merge** — look, do not ask |  |"),
       "SHP-CYC-001")
p.case("② una etapa desaparece de la tabla",
       lambda: edit("| 12 | **DELETE the branch** — local and remote, ⚠️ with its exceptions | §8 |", ""),
       "SHP-CYC-001")
p.case("③ el techo de agrupación no declarado",
       lambda: edit("items_per_proposal: 4", "N: 4"), "SHP-GRP-001")


# ⭐ Move the gate OUT of the hooks directory, not to a sibling name: a probe
# that hides a file next to itself is still leaving it where the detector
# looks, and then it reports a working check as undetected.
STASH = os.path.join(tempfile.gettempdir(), "zzprobe-gate-stash")


def hide_gate():
    shutil.move(HOOK, STASH)


def restore_gate():
    if os.path.exists(STASH):
        shutil.move(STASH, HOOK)
        os.chmod(HOOK, 0o755)


p.clean()
hide_gate()
code, out, err = p.run()
hit = "SHP-LCK-001" in out
print("  %-46s %s %s" % ("④ declara 🔒 y no hay candado", "✅" if hit else "🔴",
                         "FAIL" if hit else "NOT_DETECTED"))
p.results.append(("④ 🔒 sin candado", "FAIL" if hit else "NOT_DETECTED"))
restore_gate()
p.clean()

p.inverse("⑤ el estado real", lambda: None)

# ── B · the gate is INVOKED, not merely found
print("\n═══ B · EL CANDADO SE INVOCA, no se da por presente ═══\n")
tmp = tempfile.mkdtemp(prefix="zzprobe-git-")
try:
    env = dict(os.environ, GIT_AUTHOR_NAME="probe", GIT_AUTHOR_EMAIL="p@x",
               GIT_COMMITTER_NAME="probe", GIT_COMMITTER_EMAIL="p@x")
    run = lambda *a: subprocess.run(a, cwd=tmp, capture_output=True, text=True, env=env)
    run("git", "init", "-q", "-b", "main")
    open(os.path.join(tmp, "f.txt"), "w").write("x\n")
    run("git", "add", "-A")
    run("git", "commit", "-qm", "seed", "--no-verify")
    os.makedirs(os.path.join(tmp, ".git", "hooks"), exist_ok=True)
    shutil.copy(HOOK, os.path.join(tmp, ".git", "hooks", "pre-commit"))
    os.chmod(os.path.join(tmp, ".git", "hooks", "pre-commit"), 0o755)

    # ⛔ on the base → must refuse
    open(os.path.join(tmp, "f.txt"), "a").write("y\n")
    run("git", "add", "-A")
    r = run("git", "commit", "-qm", "on base")
    refused = r.returncode != 0 and "REFUSED" in (r.stderr + r.stdout)
    print("  %-46s %s %s" % ("⑥ commit sobre la base", "✅" if refused else "🔴",
                             "RECHAZADO" if refused else "PASO — el candado no mide"))
    p.results.append(("⑥ commit sobre la base", "FAIL" if refused else "NOT_DETECTED"))

    # ✅ on a branch → must pass
    run("git", "switch", "-qc", "feat/x")
    r = run("git", "commit", "-qm", "on branch")
    passed = r.returncode == 0
    print("  %-46s %s %s" % ("⑦ commit sobre una rama", "✅" if passed else "🔴",
                             "NO dispara (correcto)" if passed else "falso positivo"))
    p.results.append(("⑦ commit sobre una rama", "PASS" if passed else "FALSE_POSITIVE"))

    # ⭐ the escape hatch works, and it is loud
    run("git", "switch", "-q", "main")
    open(os.path.join(tmp, "f.txt"), "a").write("z\n")
    run("git", "add", "-A")
    r = run("git", "commit", "-qm", "bypass", "--no-verify")
    bypassed = r.returncode == 0
    print("  %-46s %s %s" % ("⑧ la vía de escape funciona",
                             "✅" if bypassed else "🔴",
                             "permitida y con rastro" if bypassed
                             else "un candado sin salida se borra"))
    p.results.append(("⑧ vía de escape", "PASS" if bypassed else "FALSE_POSITIVE"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

p.crash_guard()
sys.exit(0 if p.report() else 1)
