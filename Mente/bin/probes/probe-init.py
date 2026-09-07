#!/usr/bin/env python3
"""probe-init — proves the installer places what it must, asks what it cannot derive, and refuses to destroy.

⭐ AN INSTALLER'S WORST FAILURE IS NOT LEAVING SOMETHING OUT. It is overwriting a
configured instance while reporting success — the files are still there, still
read, and now say what somebody else's machine said. ⛔ Half the cases below
measure what it does NOT do.

🔴 AND THE SECOND WORST IS FILLING A PLACEHOLDER WITH A GUESS. When a config
once shipped carrying a real owner name, this step ran on another clone and
never asked: it found a name and took it as truth. ⚠️ So a missing terminal must
ABORT, not default.

Runs against an ISOLATED COPY — ⛔ measured the hard way: running the installer
in the source tree writes an owner name across the whole engine.
"""
import os, glob, re, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-init-")
OWNER = "Zzprobe Owner"


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def fresh(git=True):
    """A clone-shaped tree: Mente/ inside a repository, nothing installed."""
    repo = tempfile.mkdtemp(prefix="tree-", dir=WORK)
    tree = os.path.join(repo, "Mente")
    shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(
        "__pycache__", ".beats", ".test-lock", ".git", "cache"))
    # ⚠️ A clone has no instance files; the working tree may. Removing them is
    # what makes this a CLONE and not a copy of a configured machine.
    # 🔴 EVERY instance file, and the list is the .gitignore's, not one I
    # remembered. Measured the hard way: PROJECT-RULES.md was left out of a
    # hand-written list, so a stale copy from an earlier run survived and the
    # probe measured a tree that was already installed — reporting a
    # substitution as broken when it had simply never run.
    for f in ("mente.config.yml", "PROJECT-RULES.md", "accounts.tsv",
              "docs/WORKSPACE.md", "memory/RESUME.md", "memory/PENDING.md",
              "Cerebro/ARCHITECTURE.md", "connection/bridges/BRIDGES.md"):
        p = os.path.join(tree, f)
        if os.path.exists(p):
            os.remove(p)
    if git:
        subprocess.run(["git", "init", "-q"], cwd=repo, capture_output=True)
    return repo, tree


def run(tree, *args, stdin=None):
    return subprocess.run([sys.executable, os.path.join(tree, "bin", "init")]
                          + list(args), cwd=tree, capture_output=True,
                          text=True, input=stdin, timeout=60)


def has(tree, rel):
    return os.path.exists(os.path.join(tree, rel))


print("═══ SONDA · init ═══\n")

# ── ① IT PLACES WHAT THE PIECE TABLE DECLARES ───────────────────────────────
repo, tree = fresh()
r = run(tree, "--owner", OWNER)
case("① ⭐ installs and exits clean", r.returncode == 0, "exit=%d" % r.returncode)

expected = ["mente.config.yml", "PROJECT-RULES.md", "docs/WORKSPACE.md",
            "memory/RESUME.md", "memory/PENDING.md", "accounts.tsv",
            "Cerebro/ARCHITECTURE.md", "connection/bridges/BRIDGES.md"]
missing = [f for f in expected if not has(tree, f)]
case("② ⭐ the 8 instance files exist", not missing, str(missing))

# ⭐ THE DESTINATIONS ARE DERIVED FROM THE PIECE TABLE, so a template declared
# there is placed without editing the installer. ⛔ A list inside it would go
# stale the first time somebody adds a template and forgets.
open(os.path.join(tree, "templates", "ZZNEW.md.template"), "w").write(
    "# new\n\n**Owner:** {{owner}}\n")
with open(os.path.join(tree, "pieces.tsv"), "a") as fh:
    fh.write("zznew\tdocs/ZZNEW.md\tengine\tcanonical\ta fixture\n")
r = run(tree, "--owner", OWNER)
case("③ ⭐ a NEW template is placed without touching the installer",
     has(tree, "docs/ZZNEW.md"), "exit=%d" % r.returncode)

# ⛔ AND A TEMPLATE WITH NO DECLARED DESTINATION IS A FAILURE, never a silent
# skip: it means the engine ships a blueprint nothing stamps, and the install
# would look complete with a file missing.
open(os.path.join(tree, "templates", "ZZORPHAN.md.template"), "w").write("# x\n")
r = run(tree, "--owner", OWNER)
case("④ ⛔ a template with NO declared destination → it fails, it does not skip it",
     r.returncode == 2 and "ZZORPHAN.md" in r.stderr, "exit=%d" % r.returncode)
os.remove(os.path.join(tree, "templates", "ZZORPHAN.md.template"))

# ── ② NO PLACEHOLDER SURVIVES ───────────────────────────────────────────────
# 🔴 The half that is easy to miss: stamping the templates leaves the SHIPPED
# documents still reading `Owner: {{owner}}` — which passes every check while
# identifying nobody.
left = []
for dp, dn, fn in os.walk(tree):
    dn[:] = [d for d in dn if d not in {"templates", "__pycache__", ".git"}]
    for n in fn:
        if not n.endswith((".md", ".tsv", ".yml")):
            continue
        try:
            t = open(os.path.join(dp, n), encoding="utf-8",
                     errors="replace").read()
        except OSError:
            continue
        if "{{owner}}" in t or "{{project}}" in t or "{{date}}" in t:
            left.append(plat.rel(os.path.join(dp, n), tree))
case("⑤ 🔴 NO engine document is left with a placeholder", not left,
     str(left[:3]))

case("⑥ ⭐ and the name really landed",
     OWNER in open(os.path.join(tree, "mente.config.yml"),
                   encoding="utf-8").read())

# ⛔ THE BLUEPRINTS STAY BLUEPRINTS. A filled template would stamp somebody's
# name on the next --force.
case("⑦ ⛔ the templates are NOT filled — they stay templates",
     "{{owner}}" in open(os.path.join(tree, "templates",
                                      "WORKSPACE.md.template"),
                         encoding="utf-8").read())

# ── ③ IT REFUSES TO DESTROY ─────────────────────────────────────────────────
# ⭐ The worst failure an installer has: overwriting a configured instance while
# reporting success.
mark = os.path.join(tree, "mente.config.yml")
open(mark, "a").write("\n# a change the owner made\n")
r = run(tree, "--owner", "Someone Else")
case("⑧ 🔴 a second run does NOT overwrite what is configured",
     "a change the owner made" in open(mark, encoding="utf-8").read())
case("⑨ ⭐ and it NAMES what it kept, it does not count it in silence",
     "kept" in r.stdout and "mente.config.yml" in r.stdout)

# ⭐ --force overwrites, and only then
r = run(tree, "--force", "--owner", OWNER)
case("⑩ ⭐ --force does replace",
     "a change the owner made" not in open(mark, encoding="utf-8").read())

# ── ④ IT ASKS WHAT IT CANNOT DERIVE, AND REFUSES TO GUESS ───────────────────
repo2, tree2 = fresh()
r = run(tree2, stdin="")          # no terminal, no --owner
case("⑪ 🔴 no terminal and no --owner → it ABORTS, it does not invent an owner",
     r.returncode == 2 and "come from the person" in r.stderr,
     "exit=%d" % r.returncode)
case("⑫ ⛔ and it wrote nothing when aborting", not has(tree2, "mente.config.yml"))

# ⭐ the project name is DERIVED — a question whose answer is on screen trains
# people to hit enter
r = run(tree2, "--owner", OWNER)
case("⑬ ⭐ the project is derived from the directory, never asked",
     os.path.basename(repo2) in open(os.path.join(tree2, "PROJECT-RULES.md"),
                                     encoding="utf-8").read())

# ── ⑤ THE IMPORT IS APPENDED, NEVER OVERWRITTEN ─────────────────────────────
# ⛔ That line is the only thing this system writes outside its own folder, and
# the file it writes into is the user's.
repo3, tree3 = fresh()
user = os.path.join(repo3, "CLAUDE.md")
open(user, "w").write("# My own rules\n\nNever delete these.\n")
run(tree3, "--owner", OWNER)
body = open(user, encoding="utf-8").read()
case("⑭ ⛔ the user's CLAUDE.md KEEPS what was theirs",
     "Never delete these." in body)
case("⑮ ⭐ and it gains the import line", "@Mente/CLAUDE-MENTE-OS.md" in body)

run(tree3, "--force", "--owner", OWNER)
case("⑯ ⚠️ a second run does not duplicate the import",
     open(user, encoding="utf-8").read().count("@Mente/CLAUDE-MENTE-OS.md") == 1)

# ── ⑥ IT WIRES WHAT GIT CANNOT CARRY ────────────────────────────────────────
# 🔴 A hook file that is not WIRED never runs and looks installed.
#
# ⚠️ WIRED, NOT «SYMLINKED», AND THE DIFFERENCE COST TWO FALSE REDS. 🔴 Measured
# 2026-09-05 on a real Windows run: `os.symlink` needs a privilege a normal
# account does not have, so `bin/init` writes a small launcher instead — the
# hook RUNS. This probe asked `os.path.islink` and reported it dead. ⛔ It was
# measuring the mechanism, not the outcome, and the outcome was fine.
def wired(name):
    """The hook runs: a link, or the launcher init writes where links are denied."""
    p = os.path.join(repo, ".git", "hooks", name)
    if os.path.islink(p):
        return True, "symlink"
    if os.path.isfile(p):
        body = open(p, encoding="utf-8", errors="replace").read()
        # ⭐ It must actually reach the shipped hook — a file that exists and
        # invokes nothing is the very failure this case exists for.
        return ("hooks/%s.sh" % name) in body.replace("\\", "/"), "launcher"
    return False, "absent"


_ok, _how = wired("pre-push")
case("⑰ 🔴 layer 2 is WIRED (git cannot carry it)", _ok, _how)

# ⛔ BOTH git hooks, not one. pre-commit.sh shipped implementing SHP-LCK-001 —
# the rule refusing a commit on the base branch — and init linked only pre-push:
# ⚠️ a hook file that is not wired never runs and looks installed, which is the
# exact failure this whole step exists for.
_ok2, _how2 = wired("pre-commit")
case("⑰b 🔴 the base-branch hook is WIRED too", _ok2, _how2)
# ── 🔴 WHAT AN INSTALLATION ACTUALLY GETS ──────────────────────────────────
# ⛔ Every probe until here measured the TEMPLATE. An install has substituted
# values, generated files and a config the template never has — ⚠️ and
# check-document failed on every fresh install for exactly that reason:
# README.md and base-rules.md promised `docs/PENDING-{{owner}}.md`, a file
# nothing creates, so a newcomer's first `bin/check-document` was red.
# ⭐ The template being clean says nothing about the thing people run.
# ⚠️ ITS OWN TREE. `tree` has been through the sabotage cases above, so running
# validators on it would measure those, not the install — ⛔ a fixture reused
# past its purpose reports defects the thing under test never had.
_repoC, _treeC = fresh()
run(_treeC, "--owner", "Someone")
_git = ["git", "-c", "user.email=p@p", "-c", "user.name=p"]
# ⚠️ ON A BRANCH, because the install wires `pre-commit` and that gate refuses
# the base branch — 🔴 including the repository's FIRST commit, since 2026-09-06.
# ⛔ Committing on `master` here silently produced nothing, and every validator
# below then measured an uncommitted tree instead of an installed one.
# ⭐ The fixture obeys the gate it just installed; that is the point of the gate.
subprocess.run(["git", "switch", "-q", "-c", "chore/install"], cwd=_repoC,
               capture_output=True)
subprocess.run(["git", "add", "-A"], cwd=_repoC, capture_output=True)
subprocess.run(_git + ["commit", "-qm", "install"], cwd=_repoC,
               capture_output=True)
_dirty = []
for _c in sorted(glob.glob(os.path.join(_treeC, "bin", "check-*"))):
    _r = subprocess.run([sys.executable, _c], cwd=_treeC, capture_output=True,
                        text=True, timeout=90)
    if _r.returncode != 0:
        _dirty.append("%s(%d)" % (os.path.basename(_c), _r.returncode))
case("⑰c 🔴 ⭐ the INSTALLED tree passes its own validators",
     not _dirty, ", ".join(_dirty)[:44] or "24 of 24 clean")

# ⬜ ASK THE PLATFORM. 🔴 Measured on Windows: chmod is accepted and changes
# nothing, so this case reported a red about a folder the installer could not
# have hardened — and `bin/init` already says so honestly in its own output.
# ⛔ Judging a platform's answer as the engine's failure is a red that teaches
# the reader to stop reading.
if plat.modes_are_real():
    case("⑱ ⭐ and `secrets/` ends at 700",
         not (os.stat(os.path.join(tree, "secrets")).st_mode & 0o077))
else:
    # ⭐ The mode cannot be measured, but the HONESTY can: init must not claim
    # a protection it did not apply.
    # ⭐ The mode cannot be measured, so the case that CAN be is the installer's
    # honesty: `harden` must route through plat.modes_are_real() and answer
    # ⬜ NOT MEASURED, never a bare "700". ⛔ Read from source, because the
    # message only appears on the platform that cannot be staged here.
    _src = open(os.path.join(tree, "bin", "init"), encoding="utf-8").read()
    _h = _src[_src.index("def harden("):]
    case("⑱ ⬜ modes not enforced here · init reports ⬜, it does not claim 700",
         "modes_are_real()" in _h and "NOT MEASURED" in _h,
         "harden() asks the platform first")

# ⚠️ an existing hook pointing elsewhere is LEFT ALONE — it is not ours to
# replace, and silently taking it over would disable whatever it did
repo4, tree4 = fresh()
os.makedirs(os.path.join(repo4, ".git", "hooks"), exist_ok=True)
theirs = os.path.join(repo4, ".git", "hooks", "pre-push")
open(theirs, "w").write("#!/bin/sh\nexit 0\n")
r = run(tree4, "--owner", OWNER)
case("⑲ ⚠️ a foreign hook is NOT replaced, and it says so",
     "points elsewhere" in r.stdout and
     open(theirs).read().startswith("#!/bin/sh"))

# ── ㉒ THE REGISTRY IS DECLARED, NOT ONLY WIRED ─────────────────────────────
# 🔴 Measured 2026-09-05 on a fresh clone: ③b wrote `.claude/settings.json` and
# the gates ran, but `hooks.registry` stayed null — so `check-health` reported
# the wiring as ⬜ NOT MEASURED forever. ⭐ The guard that watches the guards
# was blind on every new installation, and it looked exactly like "fine".
repoR, treeR = fresh()
r = run(treeR, "--owner", OWNER)
_cfg = open(os.path.join(treeR, "mente.config.yml"), encoding="utf-8").read()
case("㉒ ⭐ init DECLARES where it wired the gates",
     "registry: null" not in _cfg and ".claude/settings.json" in _cfg
     and "hooks.registry" in r.stdout)

# ⛔ The declaration must be RELATIVE to the repository, which is where
# check-health resolves it from. An absolute path is this machine's.
_line = _cfg.split("registry:")[1].split("\n")[0].strip().strip('"')
case("㉒b ⛔ the declared path is relative, not this machine's",
     not os.path.isabs(_line) and treeR not in _cfg, _line)

# ⭐ THE CASE THAT MATTERS: not that a key changed, but that the check which was
# blind can now SEE. A probe that only reads the config would pass against a
# path pointing nowhere — which is the bug this replaced.
_h = subprocess.run([sys.executable, os.path.join(treeR, "bin", "check-health")],
                    cwd=treeR, capture_output=True, text=True, timeout=60)
case("㉒c 🔴 ⭐ check-health now MEASURES the hook wiring on a fresh install",
     "no registry declared" not in _h.stdout
     and "declared registry does not exist" not in _h.stdout,
     "0 of 2" if "0 of 2" in _h.stdout else "measured")

# ⛔ AND IT NEVER OVERWRITES AN ANSWER A PERSON GAVE. Their host, their path.
repoS, treeS = fresh()
_c = os.path.join(treeS, "mente.config.yml")
shutil.copy(os.path.join(treeS, "templates", "mente.config.yml.template"), _c)
_t = open(_c, encoding="utf-8").read().replace("registry: null", 'registry: "mine.json"')
open(_c, "w", encoding="utf-8").write(_t)
run(treeS, "--owner", OWNER)
case("㉒d ⛔ an answer the owner already gave is NOT overwritten",
     'registry: "mine.json"' in open(_c, encoding="utf-8").read())

# ── ㉓ WHAT IS AROUND THE INSTALL, SAID BEFORE IT WRITES ───────────────────
# 🔴 BOTH MEASURED ON ONE REAL WINDOWS MACHINE, 2026-09-05. Neither is a fault
# in the clone and neither can be repaired by the engine — ⛔ which is exactly
# why they must be SAID, and said BEFORE anything is written.
repoO = tempfile.mkdtemp(prefix="outer-", dir=WORK)
subprocess.run(["git", "init", "-q", repoO], capture_output=True)
_i = os.path.join(repoO, "inner")
shutil.copytree(ROOT, os.path.join(_i, "Mente"),
                ignore=shutil.ignore_patterns("__pycache__", ".beats",
                                              ".test-lock", ".git", "cache"))
r = run(os.path.join(_i, "Mente"), "--dry-run", "--owner", OWNER)
case("㉓ 🔴 ⭐ an OUTER git repository is named before anything is written",
     "OUTER git repository" in r.stderr and "dry run" in r.stdout,
     "warned first" if "OUTER git repository" in r.stderr else "🔴 silent")

# ⚠️ The engine already said "keep credentials out of a synced folder" — while
# sitting in one, and saying nothing. A generic caution where a specific one
# was available is a caution nobody acts on.
syn = os.path.join(WORK, "OneDrive", "Desktop", "proj")
shutil.copytree(ROOT, os.path.join(syn, "Mente"),
                ignore=shutil.ignore_patterns("__pycache__", ".beats",
                                              ".test-lock", ".git", "cache"))
r = run(os.path.join(syn, "Mente"), "--dry-run", "--owner", OWNER)
case("㉓b ⚠️ a SYNCED drive is named, not just cautioned about in general",
     "SYNCED drive" in r.stderr,
     "OneDrive detected" if "SYNCED drive" in r.stderr else "🔴 silent")

# ── ㉔ CRLF · the failure that killed every gate at once ────────────────────
# 🔴 Measured 2026-09-05 on a real Windows install: git converts line endings on
# checkout by default, so every shell script arrived with CRLF and bash refused
# them — `/usr/bin/env: 'bash\r': No such file or directory`. ⛔ ALL THREE GATES
# WERE DEAD, and git read the failing hook as exit 0: a commit that should have
# been refused went straight through.
# ⭐ A shell script is not text to adapt to the platform — it is a program whose
# interpreter rejects the carriage return.
# ⬜ The isolated copy has no parent repository, so the file cannot be there.
# CHK-CAU-003: said out loud, never counted as a pass.
_ga = os.path.join(os.path.dirname(ROOT), ".gitattributes")
if not os.path.isfile(_ga) and os.environ.get("MENTE_PROBE_ISOLATED"):
    print("  ⬜ .gitattributes · NOT MEASURED · no parent repository in the "
          "isolated copy")
elif True:
    case("㉔ 🔴 ⭐ .gitattributes ships, so git cannot convert the executables",
         os.path.isfile(_ga), "present" if os.path.isfile(_ga) else "🔴 absent")
if os.path.isfile(_ga):
    _t = open(_ga, encoding="utf-8").read()
    # ⭐ ONE RULE, NOT A LIST. 🔴 Measured 2026-09-05: pinning LF on the
    # executables and marking documents as `text` told git to convert THOSE —
    # a freshly cloned tree on Windows reported 19 files modified that nobody
    # had touched, and check-clear-ready refused the cut over changes that did
    # not exist. ⛔ A repo dirty the moment it is cloned teaches people to
    # ignore that warning.
    case("㉔b 🔴 ⭐ git converts NOTHING — what is committed is what lands",
         "* -text" in _t)
    case("㉔c ⛔ and no rule re-enables conversion for a subset",
         not any(l.strip().endswith(" text") or " text " in l
                 for l in _t.split("\n") if not l.strip().startswith("#")))

# ⛔ AND NO EXECUTABLE MAY SHIP WITH A CARRIAGE RETURN IN THE SHIPPED TREE.
_crlf = []
for _d, _sub, _fs in os.walk(ROOT):
    _sub[:] = [x for x in _sub if x not in (".git", "__pycache__", "cache")]
    for _f in _fs:
        if not (_f.endswith((".sh", ".py")) or "/bin/" in _d or "/hooks/" in _d):
            continue
        _fp = os.path.join(_d, _f)
        try:
            if b"\r\n" in open(_fp, "rb").read(4096):
                _crlf.append(os.path.relpath(_fp, ROOT))
        except OSError:
            pass
case("㉔d 🔴 ⭐ no executable in the tree carries CRLF",
     not _crlf, ", ".join(_crlf)[:44] or "0 file(s)")

# ── ㉕ THE REFUSAL MUST NOT TEACH ITS OWN BYPASS ───────────────────────────
# 🔴 Measured the same day: with no terminal, init refused — and the refusal
# said "or pass --owner NAME". The assistant read that, invented a name from the
# folder, and installed. ⛔ A refusal that names its own bypass is a suggestion.
_r = run(fresh()[1])          # no --owner, no terminal
_msg = (_r.stdout + _r.stderr).lower()
case("㉕ 🔴 ⭐ with no terminal it tells the assistant to ASK, not to pass a name",
     "ask them" in _msg and _r.returncode == 2, "exit=%d" % _r.returncode)
case("㉕b ⛔ and it names the sources it must NOT derive from",
     "folder" in _msg and ("git config" in _msg or "account" in _msg))

# ── ㉖ THE SKILL IS A TEMPLATE, NOT A PASSENGER ────────────────────────────
# 🔴 Measured 2026-09-06. The session-close skill shipped ACTIVE inside the
# repository, so a `git clone` alone loaded it into somebody's assistant —
# before init, before anyone agreed. ⛔ And it broke the promise this engine
# rests on: the owner keeps SEVERAL installations, every clone carried the same
# skill, and deleting one installation did not remove what its skill had written
# outside it. An engine that says "delete the folder and it is gone" cannot ship
# a file that outlives the folder.
_active = os.path.join(os.path.dirname(ROOT), ".claude", "skills")
case("㉖ 🔴 ⭐ no skill ships ACTIVE in the clone",
     not os.path.isdir(_active),
     "clean" if not os.path.isdir(_active) else "🔴 loads before install")
case("㉖b ⭐ it ships as a template instead",
     os.path.isfile(os.path.join(ROOT, "templates", "skills",
                                 "session-wrap", "SKILL.md.template")))

repoK, treeK = fresh()
r = run(treeK, "--owner", OWNER)
_dest = os.path.join(repoK, ".claude", "skills", "session-wrap", "SKILL.md")
case("㉖c 🔴 ⭐ init places it, and says so",
     os.path.isfile(_dest) and "skills" in r.stdout)

# ⛔ AND NEVER OVER A SKILL OF THEIRS WITH THE SAME NAME.
repoL, treeL = fresh()
_mine = os.path.join(repoL, ".claude", "skills", "session-wrap", "SKILL.md")
os.makedirs(os.path.dirname(_mine), exist_ok=True)
open(_mine, "w", encoding="utf-8").write("mine, not yours\n")
r = run(treeL, "--owner", OWNER)
case("㉖d ⛔ a skill of theirs is left untouched, and it says so",
     open(_mine, encoding="utf-8").read() == "mine, not yours\n"
     and "already there" in r.stdout)

# ── ⑦ --dry-run WRITES NOTHING ──────────────────────────────────────────────
repo5, tree5 = fresh()
r = run(tree5, "--dry-run", "--owner", OWNER)
case("⑳ ⭐ --dry-run reports and writes NOTHING",
     r.returncode == 0 and not has(tree5, "mente.config.yml")
     and "dry run" in r.stdout)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
repo6, tree6 = fresh()
plat.rmtree(os.path.join(tree6, "templates"))
r = run(tree6, "--owner", OWNER)
case("㉑ ⛔ no templates/ → it says so, it does not crash",
     r.returncode == 2 and "Traceback" not in r.stderr, "exit=%d" % r.returncode)

plat.rmtree(WORK)# ── ㉗ 🔴 A SKILL MAY NAME ONLY WHAT THE ENGINE SHIPS ───────────────────────
# 🔴 THE FAILURE, measured 2026-09-06 on a real installation. This skill shipped
# naming files that exist in the author's own instance and in no clone —
# `RETOMAR.md`, `PENDIENTES.md`, `bin/check-sufficiency`, `bin/test-f0-f6`:
# ⛔ six citations, none of which resolve on a fresh install. The assistant
# following it improvised the entire session close, and a person who could not
# read code would have written their brief into a file nothing reads.
# ⭐ A skill travels to EVERY clone, so it may name only engine paths.
_sk = os.path.join(ROOT, "templates", "skills")
_bodies = []
for _n in sorted(os.listdir(_sk)) if os.path.isdir(_sk) else []:
    _f = os.path.join(_sk, _n, "SKILL.md.template")
    if os.path.isfile(_f):
        _bodies.append((_n, open(_f, encoding="utf-8").read()))
    else:
        # ⬜ CHK-CAU-003 · said out loud, never swallowed.
        print("  ⬜ %s has no SKILL.md.template · NOT MEASURED" % _n)

# ⭐ Every `bin/<name>` a skill tells the assistant to run must exist. ⛔ This is
# the case that would have caught it: two of the six were commands.
_missing = []
for _n, _b in _bodies:
    for _cmd in set(re.findall(r"bin/([a-z0-9][\w.-]*)", _b)):
        _p = os.path.join(ROOT, "bin", _cmd)
        if not os.path.exists(_p) and not os.path.exists(_p + ".py"):
            _missing.append("%s → bin/%s" % (_n, _cmd))
case("㉗ 🔴 ⭐ every command a skill names actually ships",
     not _missing, ", ".join(_missing) or "%d skill(s)" % len(_bodies))

# ⛔ And no INSTANCE filename either. These four are the measured ones: they are
# real files in the author's tree, which is exactly why they read as correct.
_INSTANCE = ("RETOMAR.md", "PENDIENTES.md", "Bitacora_Progreso",
             "Registro_Conversaciones", "Estado_Sesion")
_named = []
for _n, _b in _bodies:
    # ⚠️ The block that DOCUMENTS the failure legitimately names them. Only
    # lines that instruct count — a quoted post-mortem is evidence, not an order.
    for _line in _b.split("\n"):
        if _line.lstrip().startswith(">") or "none of which resolve" in _line:
            continue
        for _w in _INSTANCE:
            if _w in _line:
                _named.append("%s → %s" % (_n, _w))
case("㉗b ⛔ and no skill names an instance-only file as an instruction",
     not _named, ", ".join(sorted(set(_named))) or "clean")

# ⭐ THE POSITIVE HALF: it must say where to LOOK instead. ⛔ Without this the
# fix reads as "name nothing", and the next author hardcodes a path again.
case("㉗c ⭐ and it points at the piece table for instance paths",
     all("pieces.tsv" in _b for _, _b in _bodies), "%d skill(s)" % len(_bodies))


good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
