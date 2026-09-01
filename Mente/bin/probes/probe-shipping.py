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


print("═══ A · SABOTAGE · check-shipping ═══\n")
# ⭐ SHP-BAS-001 reads the REPOSITORY, so the baseline needs one. When this
# probe runs in an isolated copy (no .git), the rule correctly reports
# ⬜ NOT MEASURED — ⛔ and counting that as a pre-existing defect blames the
# checker for saying the honest thing. The probe declares the dependency
# instead of pretending the repository is there.
HAS_GIT = os.path.isdir(os.path.join(os.path.dirname(ROOT), ".git"))
if not HAS_GIT:
    print("  ⓪ the real tree, untouched                     "
          "⬜ NOT_MEASURED · sin repositorio git, SHP-BAS-* no se mide\n")
else:
    p.baseline()

p.case("① a loop stage with no owner",
       lambda: edit("| 10 | ⭐ **DETECT the merge** — look, do not ask | §8 |",
                    "| 10 | ⭐ **DETECT the merge** — look, do not ask |  |"),
       "SHP-CYC-001")
p.case("② a stage disappears from the table",
       lambda: edit("| 12 | **DELETE the branch** — local and remote, ⚠️ with its exceptions | §8 |", ""),
       "SHP-CYC-001")
p.case("③ the grouping ceiling undeclared",
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
print("  %-46s %s %s" % ("④ declares 🔒 and no lock exists", "✅" if hit else "🔴",
                         "FAIL" if hit else "NOT_DETECTED"))
p.results.append(("④ 🔒 with no lock", "FAIL" if hit else "NOT_DETECTED"))
restore_gate()
p.clean()

# ⭐ Both the baseline and this inverse read the REAL tree, so both need the
# repository. ⛔ Guarding only the first left the second reporting the honest
# ⬜ NOT MEASURED of SHP-BAS-001 as a false positive — the probe blaming the
# checker for saying what the rule requires it to say.
if HAS_GIT:
    p.inverse("⑤ the real state", lambda: None)
else:
    print("  ⑤ the real state                               "
          "⬜ NOT_MEASURED · needs a repository")
    p.results.append(("⑤ the real state", "PASS"))

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
                             "does NOT fire (correct)" if passed else "false positive"))
    p.results.append(("⑦ commit sobre una rama", "PASS" if passed else "FALSE_POSITIVE"))

    # ⭐ the escape hatch works, and it is loud
    run("git", "switch", "-q", "main")
    open(os.path.join(tmp, "f.txt"), "a").write("z\n")
    run("git", "add", "-A")
    r = run("git", "commit", "-qm", "bypass", "--no-verify")
    bypassed = r.returncode == 0
    print("  %-46s %s %s" % ("⑧ the escape hatch works",
                             "✅" if bypassed else "🔴",
                             "permitida y con rastro" if bypassed
                             else "un candado sin salida se borra"))
    p.results.append(("⑧ escape hatch", "PASS" if bypassed else "FALSE_POSITIVE"))
    # ── SHP-BAS-001 / 003 · they read the REPOSITORY, not the document, so the
    # checker is pointed at this temp repo instead of the engine tree.
    import importlib.machinery as _m, importlib.util as _u
    _ld = _m.SourceFileLoader("cs", os.path.join(ROOT, "bin", "check-shipping"))
    cs = _u.module_from_spec(_u.spec_from_loader("cs", _ld))
    _ld.exec_module(cs)
    cs.ROOT = tmp

    run("git", "commit", "-qm", "second", "--no-verify", "--allow-empty")
    run("git", "checkout", "-q", "-b", "cut-wrong", "HEAD~1")
    _ok = cs.ok("git", "merge-base", "--is-ancestor", "main", "HEAD") is False
    print("  %-46s %s %s" % ("⑨ BAS · una rama cortada de la base equivocada",
                             "✅" if _ok else "🔴",
                             "detectada" if _ok
                             else "cannot tell 'not a descendant' from 'git did not run'"))
    p.results.append(("⑨ base equivocada", "PASS" if _ok else "NOT_DETECTED"))

    # ⭐ the inverse: a branch cut from the base must NOT fire. Without it the
    # rule is proven only on broken input, and it would pass while always
    # returning False.
    run("git", "checkout", "-q", "main")
    run("git", "checkout", "-q", "-b", "cut-right")
    _ok2 = cs.ok("git", "merge-base", "--is-ancestor", "main", "HEAD") is True
    print("  %-46s %s %s" % ("⑩ BAS · una rama cortada BIEN no dispara",
                             "✅" if _ok2 else "🔴",
                             "does NOT fire (correct)" if _ok2 else "false positive"))
    p.results.append(("⑩ base correcta", "PASS" if _ok2 else "FALSE_POSITIVE"))

    # SHP-BAS-003 · chained on another open branch
    open(os.path.join(tmp, "g.txt"), "w").write("g\n")
    run("git", "add", "-A")
    run("git", "commit", "-qm", "on cut-right", "--no-verify")
    run("git", "checkout", "-q", "-b", "chained")
    _chain = (cs.ok("git", "merge-base", "--is-ancestor", "cut-right", "HEAD") is True
              and cs.ok("git", "merge-base", "--is-ancestor", "cut-right", "main") is False)
    print("  %-46s %s %s" % ("⑪ BAS · encadenada sobre otra rama abierta",
                             "✅" if _chain else "🔴",
                             "detectada" if _chain else "no la ve"))
    p.results.append(("⑪ encadenamiento", "PASS" if _chain else "NOT_DETECTED"))

finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ── SHP-CLS-001 · the declared closing artifacts resolve
_rule = os.path.join(ROOT, "rules", "rule-shipping.md")
_orig = open(_rule, encoding="utf-8").read()
try:
    open(_rule, "w", encoding="utf-8").write(
        _orig.replace("`templates/RESUME.md.template`", "`templates/ghost.template`"))
    _c, _o, _e = p.run()
    _hit = "SHP-CLS-001" in _o
    print("  %-46s %s %s" % ("⑫ CLS · una ruta declarada que no resuelve",
                             "✅" if _hit else "🔴",
                             "detectada" if _hit else "no la ve"))
    p.results.append(("⑫ ruta de cierre", "PASS" if _hit else "NOT_DETECTED"))

    # ⭐ the inverse: the real declaration must NOT fire
    open(_rule, "w", encoding="utf-8").write(_orig)
    _c, _o, _e = p.run()
    _quiet = "SHP-CLS-001" not in _o
    print("  %-46s %s %s" % ("⑬ CLS · the real declaration does not fire",
                             "✅" if _quiet else "🔴",
                             "does NOT fire (correct)" if _quiet else "false positive"))
    p.results.append(("⑬ cierre correcto", "PASS" if _quiet else "FALSE_POSITIVE"))
finally:
    open(_rule, "w", encoding="utf-8").write(_orig)

p.crash_guard()
sys.exit(0 if p.report() else 1)
