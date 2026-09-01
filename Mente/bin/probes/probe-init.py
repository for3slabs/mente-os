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
import os, shutil, subprocess, sys, tempfile

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
case("① ⭐ instala y termina bien", r.returncode == 0, "exit=%d" % r.returncode)

expected = ["mente.config.yml", "PROJECT-RULES.md", "docs/WORKSPACE.md",
            "memory/RESUME.md", "memory/PENDING.md", "accounts.tsv",
            "Cerebro/ARCHITECTURE.md", "connection/bridges/BRIDGES.md"]
missing = [f for f in expected if not has(tree, f)]
case("② ⭐ los 8 archivos de instancia existen", not missing, str(missing))

# ⭐ THE DESTINATIONS ARE DERIVED FROM THE PIECE TABLE, so a template declared
# there is placed without editing the installer. ⛔ A list inside it would go
# stale the first time somebody adds a template and forgets.
open(os.path.join(tree, "templates", "ZZNEW.md.template"), "w").write(
    "# new\n\n**Owner:** {{owner}}\n")
with open(os.path.join(tree, "pieces.tsv"), "a") as fh:
    fh.write("zznew\tdocs/ZZNEW.md\tengine\tcanonical\ta fixture\n")
r = run(tree, "--owner", OWNER)
case("③ ⭐ una plantilla NUEVA se coloca sin tocar el instalador",
     has(tree, "docs/ZZNEW.md"), "exit=%d" % r.returncode)

# ⛔ AND A TEMPLATE WITH NO DECLARED DESTINATION IS A FAILURE, never a silent
# skip: it means the engine ships a blueprint nothing stamps, and the install
# would look complete with a file missing.
open(os.path.join(tree, "templates", "ZZORPHAN.md.template"), "w").write("# x\n")
r = run(tree, "--owner", OWNER)
case("④ ⛔ una plantilla SIN destino declarado → falla, no la salta",
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
            left.append(os.path.relpath(os.path.join(dp, n), tree))
case("⑤ 🔴 NINGÚN documento del motor queda con placeholder", not left,
     str(left[:3]))

case("⑥ ⭐ y el nombre entró de verdad",
     OWNER in open(os.path.join(tree, "mente.config.yml"),
                   encoding="utf-8").read())

# ⛔ THE BLUEPRINTS STAY BLUEPRINTS. A filled template would stamp somebody's
# name on the next --force.
case("⑦ ⛔ las plantillas NO se rellenan — siguen siendo plantillas",
     "{{owner}}" in open(os.path.join(tree, "templates",
                                      "WORKSPACE.md.template"),
                         encoding="utf-8").read())

# ── ③ IT REFUSES TO DESTROY ─────────────────────────────────────────────────
# ⭐ The worst failure an installer has: overwriting a configured instance while
# reporting success.
mark = os.path.join(tree, "mente.config.yml")
open(mark, "a").write("\n# a change the owner made\n")
r = run(tree, "--owner", "Someone Else")
case("⑧ 🔴 una segunda pasada NO pisa lo ya configurado",
     "a change the owner made" in open(mark, encoding="utf-8").read())
case("⑨ ⭐ y NOMBRA lo que conservó, no lo cuenta en silencio",
     "kept" in r.stdout and "mente.config.yml" in r.stdout)

# ⭐ --force overwrites, and only then
r = run(tree, "--force", "--owner", OWNER)
case("⑩ ⭐ --force sí reemplaza",
     "a change the owner made" not in open(mark, encoding="utf-8").read())

# ── ④ IT ASKS WHAT IT CANNOT DERIVE, AND REFUSES TO GUESS ───────────────────
repo2, tree2 = fresh()
r = run(tree2, stdin="")          # no terminal, no --owner
case("⑪ 🔴 sin terminal y sin --owner → ABORTA, no inventa un dueño",
     r.returncode == 2 and "Guessing an owner" in r.stderr,
     "exit=%d" % r.returncode)
case("⑫ ⛔ y no escribió nada al abortar", not has(tree2, "mente.config.yml"))

# ⭐ the project name is DERIVED — a question whose answer is on screen trains
# people to hit enter
r = run(tree2, "--owner", OWNER)
case("⑬ ⭐ el proyecto se deriva del directorio, no se pregunta",
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
case("⑭ ⛔ el CLAUDE.md del usuario CONSERVA lo suyo",
     "Never delete these." in body)
case("⑮ ⭐ y gana la línea del import", "@Mente/CLAUDE-MENTE-OS.md" in body)

run(tree3, "--force", "--owner", OWNER)
case("⑯ ⚠️ una segunda pasada no duplica el import",
     open(user, encoding="utf-8").read().count("@Mente/CLAUDE-MENTE-OS.md") == 1)

# ── ⑥ IT WIRES WHAT GIT CANNOT CARRY ────────────────────────────────────────
# 🔴 A hook file that is not linked NEVER RUNS and looks installed.
case("⑰ 🔴 la capa 2 queda ENLAZADA (git no puede llevarla)",
     os.path.islink(os.path.join(repo, ".git", "hooks", "pre-push")))
case("⑱ ⭐ y `secrets/` queda en 700",
     not (os.stat(os.path.join(tree, "secrets")).st_mode & 0o077))

# ⚠️ an existing hook pointing elsewhere is LEFT ALONE — it is not ours to
# replace, and silently taking it over would disable whatever it did
repo4, tree4 = fresh()
os.makedirs(os.path.join(repo4, ".git", "hooks"), exist_ok=True)
theirs = os.path.join(repo4, ".git", "hooks", "pre-push")
open(theirs, "w").write("#!/bin/sh\nexit 0\n")
r = run(tree4, "--owner", OWNER)
case("⑲ ⚠️ un hook ajeno NO se reemplaza, y lo dice",
     "points elsewhere" in r.stdout and
     open(theirs).read().startswith("#!/bin/sh"))

# ── ⑦ --dry-run WRITES NOTHING ──────────────────────────────────────────────
repo5, tree5 = fresh()
r = run(tree5, "--dry-run", "--owner", OWNER)
case("⑳ ⭐ --dry-run informa y NO escribe",
     r.returncode == 0 and not has(tree5, "mente.config.yml")
     and "dry run" in r.stdout)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
repo6, tree6 = fresh()
shutil.rmtree(os.path.join(tree6, "templates"))
r = run(tree6, "--owner", OWNER)
case("㉑ ⛔ sin templates/ → lo dice, no revienta",
     r.returncode == 2 and "Traceback" not in r.stderr, "exit=%d" % r.returncode)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d de %d correctos" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  restos: %s" % ("ninguno" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
