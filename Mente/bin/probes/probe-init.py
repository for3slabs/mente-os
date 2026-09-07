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
import ast, os, glob, json, re, shutil, subprocess, sys, tempfile
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

# ── ⑮b 🔴 AN `@import` IS A POINTER, NOT AN INSTRUCTION THAT RUNS ───────────
# 🔴 THE FAILURE, measured 2026-09-07 on a real Windows install. The project
# `CLAUDE.md` was 136 bytes: a comment and one `@Mente/...` line. The owner
# said the assistant "has it but does not read it — it does not recognise where
# it goes, how to behave, or how to start working." ⛔ It reached its first turn
# never having been told to read RESUME, to check for an open block, or how to
# close a session. ⭐ The mature instance that DOES work carries the same words
# INSIDE its CLAUDE.md, 8.5 KB of them — one hop closer, and that hop is the
# whole difference between installed and used.
_c = open(user, encoding="utf-8").read()
case("⑮b 🔴 ⭐ the startup lives INSIDE CLAUDE.md, not only behind the import",
     "## 🚀 STARTUP" in _c and len(_c) > 1200, "%d bytes" % len(_c))

# ⭐ AND IT MUST CARRY THE FOUR THINGS A FIRST TURN NEEDS. ⛔ A startup block
# that names none of them is a heading: it looks installed and decides nothing.
_need = {"read RESUME first": "RESUME.md",
         "check for an open block": "work/blocks/active",
         "how the session ends": "/session-wrap",
         "the refusal before /clear": "check-clear-ready"}
_absent = [k for k, v in _need.items() if v not in _c]
case("⑮c 🔴 ⭐ and it names what the first turn must decide",
     not _absent, ", ".join(_absent) or "4 of 4")

# ⛔ AND IT IS APPENDED BEFORE THE IMPORT, never after: what comes after a
# pointer is read only by whoever followed the pointer.
# ⚠️ `find`, not `index`: a missing block must give a VERDICT here, not a
# ValueError. ⛔ CHK-CAU-002 — measured while sabotage-testing this very case:
# removing the block crashed the probe and it still exited 0, so the battery
# would have counted the whole file green.
_i, _j = _c.find("## 🚀 STARTUP"), _c.find("@Mente/CLAUDE-MENTE-OS.md")
case("⑮d ⛔ the startup precedes the import line, not the other way round",
     _i >= 0 and _j >= 0 and _i < _j, "startup@%d import@%d" % (_i, _j))

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

# ── ㉖e 🔴 THE WHOLE INTERFACE IS A `/command`, NOT A SCRIPT TO REMEMBER ────
# 🔴 THE FAILURE, measured 2026-09-07 on a real Windows install. The owner said:
# "it is installed, it uses it now and then, but it has not read how it must
# behave, where it goes, or how to start working." ⛔ Only ONE of the four things
# a person says out loud existed as a `/command`: `/session-wrap`. Turning the
# system on, off, or asking whether it is on were scripts under `bin/`, so the
# assistant had to REMEMBER them — and what is only remembered is used now and
# then. ⭐ A `/` menu is the one surface a person sees without being told.
_want = ("session-wrap", "mente-status", "mente-pause")
_gone = [n for n in _want
         if not os.path.isfile(os.path.join(repoK, ".claude", "skills", n,
                                            "SKILL.md"))]
case("㉖e 🔴 ⭐ every spoken command installs as a /command",
     not _gone, ", ".join(_gone) or "%d of %d" % (len(_want), len(_want)))

# ⭐ AND EACH ONE MUST SAY WHEN TO FIRE. ⛔ A skill whose `description` does not
# carry the words a person actually says is a skill the assistant never selects
# — installed, listed, and silent, which is the same failure one layer along.
_mute = []
for _n in _want:
    _f = os.path.join(repoK, ".claude", "skills", _n, "SKILL.md")
    if not os.path.isfile(_f):
        continue                       # ⬜ already reported by ㉖e
    _head = open(_f, encoding="utf-8").read().split("---", 2)[1]
    if "description:" not in _head or "Use " not in _head:
        _mute.append(_n)
case("㉖f ⛔ and each says WHEN to fire, in the words a person uses",
     not _mute, ", ".join(_mute) or "%d skill(s)" % len(_want))

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

# ── ㉗ 🔴 A SKILL MAY NAME ONLY WHAT THE ENGINE SHIPS ───────────────────────
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

# ── ㉘ 🔴 WHAT IS GENERATED IS NOT CONVERTED EITHER ─────────────────────────
# 🔴 THE FAILURE, measured 2026-09-06 on a real Windows install. Every file this
# script writes went through a plain `open(..., "w")`, and on Windows Python
# turns each "\n" into "\r\n" — ⛔ so the Claude Code skill landed with CRLF, its
# YAML frontmatter did not parse, and `/session-wrap` was simply ABSENT from the
# person's command menu. ⚠️ The install reported success and the command was
# gone: nothing said the two were related.
# ⭐ `.gitattributes` already refuses conversion for the same reason; the
# installer was the one place still doing it. ⛔ A generated file is a shipped
# file — the rule does not stop at the repository boundary.
_crlf = []
for _root, _dirs, _files in os.walk(_repoC):
    # ⚠️ `.git` holds packed objects and `__pycache__` compiled bytecode: both
    # are binary and neither was written by this installer. 🔴 Found once the
    # teardown moved to the end and this case finally ran — a probe measuring
    # Python's own .pyc files reports the interpreter, not the engine.
    _parts = _root.split(os.sep)
    if ".git" in _parts or "__pycache__" in _parts:
        _dirs[:] = []
        continue
    for _f in _files:
        _p = os.path.join(_root, _f)
        try:
            if b"\r\n" in open(_p, "rb").read():
                _crlf.append(os.path.relpath(_p, _repoC))
        except OSError:
            # ⬜ CHK-CAU-003 · said out loud, never swallowed.
            _crlf.append("⬜ unreadable: " + os.path.relpath(_p, _repoC))
case("㉘ 🔴 ⭐ nothing the installer generates carries CRLF",
     not _crlf, ", ".join(sorted(_crlf))[:44] or "0 file(s)")

# 🔴 FOUND BY SABOTAGING THE CASE ABOVE: on a POSIX kernel Python translates
# nothing, so removing `newline=""` left it green — ⛔ the case only fails on
# the platform where nobody runs the battery, which is the same as not measuring
# it. ⭐ So the SOURCE is read too: every write of a generated file must go
# through the one writer that disables translation. ⚠️ Reading code is weaker
# than reading output, and it is asserted here BECAUSE the output cannot answer
# on this platform — stated, not hidden.
# ⚠️ Read from the PARSED source, not the raw text: the post-mortem inside
# `write()` quotes the broken call verbatim, and a probe grepping the file
# reported the explanation of the bug as the bug — measured while writing this.
# ⭐ `ast` sees calls; it does not see prose.
_src = open(os.path.join(ROOT, "bin", "init"), encoding="utf-8").read()
_raw, _unsafe = [], []
for _node in ast.walk(ast.parse(_src)):
    if not (isinstance(_node, ast.Call)
            and getattr(_node.func, "id", "") == "open"):
        continue
    _mode = next((a.value for a in _node.args[1:]
                  if isinstance(a, ast.Constant)), "r")
    if "w" not in str(_mode) and "a" not in str(_mode):
        continue
    _raw.append("line %d" % _node.lineno)
    if not any(k.arg == "newline" for k in _node.keywords):
        _unsafe.append("line %d" % _node.lineno)
case("㉘c 🔴 ⭐ every generated-file write disables translation",
     not _unsafe, ", ".join(_unsafe)[:44] or "%d write(s), all safe" % len(_raw))

# ⭐ AND THE SKILL SPECIFICALLY, because its frontmatter is what breaks: a
# `/command` that does not appear is indistinguishable from one never installed.
_sk = os.path.join(_repoC, ".claude", "skills")
_bad = []
for _n in sorted(os.listdir(_sk)) if os.path.isdir(_sk) else []:
    _f = os.path.join(_sk, _n, "SKILL.md")
    if not os.path.isfile(_f):
        _bad.append("%s has no SKILL.md" % _n)
        continue
    _raw = open(_f, "rb").read()
    # ⛔ The frontmatter must open on the very first bytes and parse as lines.
    if b"\r" in _raw or not _raw.startswith(b"---\n"):
        _bad.append("%s frontmatter would not parse" % _n)
case("㉘b 🔴 ⭐ the installed skill's frontmatter parses",
     not _bad, ", ".join(_bad)[:44] or "clean")

# ── ㉙ 🔴 THE VOICE IS PLACED AND SELECTED — both, or neither counts ────────
# 🔴 THE FAILURE, measured 2026-09-06 on a real installation. The engine ships
# `memory/principles/owner-0-voice.md` — 264 lines describing how it speaks —
# and NOTHING read it: zero mentions of `outputStyle` in this installer or in
# the settings template. A fresh install answered in the assistant's default
# voice while carrying the doctrine of another one. ⛔ The owner said it: "the
# way of answering is not active".
# ⭐ A style placed and not selected is the same unread document, one folder on.
_style_dir = os.path.join(_repoC, ".claude", "output-styles")
_styles = sorted(os.listdir(_style_dir)) if os.path.isdir(_style_dir) else []
case("㉙ 🔴 ⭐ the install places an output style",
     bool(_styles), ", ".join(_styles) or ("none · dir=%s" % os.path.isdir(_style_dir)))

_cfg = os.path.join(_repoC, ".claude", "settings.json")
_chosen = ""
if os.path.isfile(_cfg):
    try:
        _chosen = json.load(open(_cfg, encoding="utf-8")).get("outputStyle", "")
    except (ValueError, OSError):
        _chosen = ""
case("㉙b 🔴 ⭐ and SELECTS it — the half that makes the other half real",
     bool(_chosen), _chosen or "not selected")

# ⛔ It must never take a voice the owner already chose. Their file, their call.
_t2 = os.path.join(tempfile.mkdtemp(prefix="tree-voice-", dir=WORK), "repo")
os.makedirs(os.path.join(_t2, ".claude"))
shutil.copytree(ROOT, os.path.join(_t2, "Mente"))
open(os.path.join(_t2, ".claude", "settings.json"), "w",
     encoding="utf-8", newline="").write('{"outputStyle":"theirs"}')
subprocess.run([sys.executable, os.path.join(_t2, "Mente", "bin", "init"),
                "--owner", "X"], capture_output=True, text=True, timeout=120)
_after = json.load(open(os.path.join(_t2, ".claude", "settings.json"),
                        encoding="utf-8")).get("outputStyle")
case("㉙c ⛔ and never over a style they already chose",
     _after == "theirs", _after or "gone")
plat.rmtree(os.path.dirname(_t2))

# ── ㉚ THE ENGINE'S OWN COMMANDS ARE PRE-APPROVED ───────────────────────────
# 🔴 Measured the same run: a permission prompt stopped `bin/init` and the
# assistant answered "open PowerShell and paste this command". ⚠️ Asking the
# owner to approve their own tool, one command at a time, is what turns a
# walkthrough into homework.
_perm = {}
if os.path.isfile(_cfg):
    try:
        _perm = json.load(open(_cfg, encoding="utf-8")).get("permissions", {})
    except (ValueError, OSError):
        _perm = {}
_allow = _perm.get("allow", []) if isinstance(_perm, dict) else []
case("㉚ ⭐ the engine's read-and-report commands are pre-approved",
     any("bin/status" in a for a in _allow), "%d entry(ies)" % len(_allow))
# ⛔ And nothing here may hand out a general shell — that is not ours to grant.
_broad = [a for a in _allow if a.strip() in ("Bash", "Bash(*)", "Bash(*:*)")]
case("㉚b ⛔ and no entry grants a general shell", not _broad,
     ", ".join(_broad) or "none")


# ── ㉛ 🔴 AN INTERPRETER THAT WAS SEEN TO RUN ───────────────────────────────
# 🔴 THE FAILURE, measured 2026-09-07 on a real Windows install. `sys.executable`
# resolved to a Microsoft Store EXECUTION ALIAS — `WindowsApps/…/python.exe`, a
# 2-byte stub that a terminal can start and a hook cannot. It was stamped into
# every gate, so NOT ONE ever ran: `Mente/.beats/` was never created. ⛔ The
# install reported success and the entire enforcement layer was dead.
# ⚠️ The file existed. Existence was never the question.
_cmds = []
_cfg2 = os.path.join(_repoC, ".claude", "settings.json")
if os.path.isfile(_cfg2):
    try:
        _h = json.load(open(_cfg2, encoding="utf-8")).get("hooks", {})
        for _grp in [g for v in _h.values() for g in v]:
            for _hk in _grp.get("hooks", []):
                _cmds.append(_hk.get("command", ""))
    except (ValueError, OSError):
        pass
# ⭐ The interpreter is the first token, quoted or not. It must START.
_dead = []
for _c in _cmds:
    _exe = re.match(r'"([^"]+)"|(\S+)', _c)
    _exe = (_exe.group(1) or _exe.group(2)) if _exe else ""
    if not _exe:
        continue
    try:
        _r = subprocess.run([_exe, "--version"], capture_output=True, timeout=15)
        if _r.returncode != 0 or not (_r.stdout or _r.stderr).strip():
            _dead.append(os.path.basename(_exe))
    except (OSError, subprocess.SubprocessError):
        _dead.append(os.path.basename(_exe))
case("㉛ 🔴 ⭐ every interpreter a hook names actually STARTS",
     not _dead, ", ".join(sorted(set(_dead))) or "%d hook(s)" % len(_cmds))
# ⛔ And the bare name is never stamped on Windows: `bash` there is the WSL
# launcher, which cannot open a C:\ path — measured, every shell hook exit 127.
case("㉛b ⛔ and no hook is left with a bare interpreter name",
     not any(re.match(r'"?(python3?|bash)"?\s', _c) for _c in _cmds),
     "%d hook(s)" % len(_cmds))

# 🔴 A PATH WITH A SPACE MUST SURVIVE THE STAMP. Measured 2026-09-07 on a real
# Windows install: the substitution stripped the closing quote so the
# interpreter ran on into its argument, which works until the path contains a
# space. `C:\Program Files\Git\bin\bash.exe` arrived unterminated, the shell
# split it, and `session-start` died with `C:Program: command not found`.
# ⛔ Not one beat from that hook, so RESUME.md was never written and the memory
# the whole system rests on stayed the shipped template.
# ⚠️ ㉛ above runs the interpreter, which cannot catch this on a POSIX kernel —
# there are no spaces in `/usr/bin/bash`. ⭐ So the substitution is exercised
# directly, with a path that has one, on every platform.
_ns = {}
_isrc = open(os.path.join(ROOT, "bin", "init"), encoding="utf-8").read()
_a = _isrc.index("        def _cmd(argv):")
_b = _isrc.index("        body = body.replace('\"python3 ")
exec(_isrc[_a:_b].replace("        ", "", 1).replace("\n        ", "\n"), _ns)
_tpl = '{"command": "bash \\"$DIR/x.sh\\""}'
_spaced = "C:\\Program Files\\Git\\bin\\bash.exe"
_ok, _why = False, ""
try:
    _stamped = _tpl.replace('"bash ', _ns["_cmd"]([_spaced]))
    _parsed = json.loads(_stamped)          # ⛔ it must still be valid JSON
    _argv = __import__("shlex").split(_parsed["command"])
    _ok = _argv[0] == _spaced
    _why = "argv[0]=%r" % _argv[0]
except Exception as _e:                                    # noqa: BLE001
    _why = "%s: %s" % (type(_e).__name__, _e)
case("㉛c 🔴 ⭐ an interpreter path WITH A SPACE survives the stamp",
     _ok, _why[:52])

# ── ㉜ 🔴 A STAMPED FILE IS NOT ITS OWN MOULD ───────────────────────────────
# 🔴 Measured 2026-09-07: nine templates open with `<!-- ⚠️ TEMPLATE — bin/init
# copies this to … -->`, and the installer copied it through. The person's own
# `memory/RESUME.md` began by saying it was a template and that "you never write
# this file by hand". ⛔ No validator caught it, and the assistant read it as an
# instruction: the scaffolding was teaching it the memory was not its to fill.
_scaffolded = []
for _root, _dirs, _files in os.walk(os.path.join(_repoC, "Mente")):
    if "__pycache__" in _root.split(os.sep) or "templates" in _root.split(os.sep):
        _dirs[:] = [d for d in _dirs if d != "__pycache__"]
        if "templates" in _root.split(os.sep):
            continue
    for _f in _files:
        if not _f.endswith((".md", ".yml", ".tsv")):
            continue
        _p = os.path.join(_root, _f)
        try:
            if "TEMPLATE —" in open(_p, encoding="utf-8",
                                    errors="replace").read(400):
                _scaffolded.append(os.path.relpath(_p, _repoC))
        except OSError:
            _scaffolded.append("⬜ unreadable: " + _f)
case("㉜ 🔴 ⭐ no installed file still carries its template scaffolding",
     not _scaffolded, ", ".join(sorted(_scaffolded))[:44] or "clean")

# 🔴 THE TEARDOWN GOES LAST. Found 2026-09-06: an insertion left this line
# glued to a comment ABOVE the cases that read the installed tree, so ㉗ and
# ㉘ measured a directory that had just been deleted — ⛔ every one of them
# green because there was nothing left to be wrong.
plat.rmtree(WORK)

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
