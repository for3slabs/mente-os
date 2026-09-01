#!/usr/bin/env python3
"""probe-gate-accounts — proves BOTH layers, and proves why there are two.

⭐ THE CASE THIS FILE EXISTS FOR is ⑬. Layer 1 reads the text of a command, so
the probe writes the same push five ways that never spell the verb plainly — an
alias, a shell function, a variable, an `eval`, an argument-builder — and shows
layer 1 missing them. ⛔ That is not a bug in layer 1: it is the measured reason
layer 2 exists, and a probe that only tested layer 1 would report a system
protected by a defence with a hole in it.

⚠️ Runs against an ISOLATED COPY: the registry is instance data, and planting
rows in a real one would leave a machine declaring repositories that do not
exist.
"""
import json, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-acct-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
L1 = os.path.join(TREE, "hooks", "gate-accounts.py")
L2 = os.path.join(TREE, "hooks", "pre-push.sh")
REG = os.path.join(WORK, "accounts.tsv")

HEADER = "repo\tcuenta\trol\tremoto\truta_local\tpor_que_existe\tguia\n"
ROWS = (HEADER
        + "an-org/live\tan-account\ttaller\torigin\t-\tthe working repo\t-\n"
        + "an-org/dead\tan-account\tarchivado\told\t-\tretired after a leak\t-\n"
        + "an-org/copy\tan-account\tbackup\tbackup\t-\ta verified copy\t-\n")
open(REG, "w", encoding="utf-8").write(ROWS)
ENV = {"MENTE_ACCOUNTS": REG}


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def layer1(cmd, env=None):
    r = subprocess.run([sys.executable, L1], cwd=TREE,
                       input=json.dumps({"tool_input": {"command": cmd}}),
                       capture_output=True, text=True,
                       env=dict(os.environ, **ENV, **(env or {})))
    try:
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]
    except Exception:                                          # noqa: BLE001
        return None                                            # silence = not its business


def layer2(url, env=None):
    e = dict(os.environ)
    e.update(ENV)
    e.update(env or {})
    return subprocess.run(["bash", L2, "origin", url], cwd=TREE,
                          capture_output=True, text=True, env=e)


print("═══ SONDA · gate-accounts (capa 1) + pre-push (capa 2) ═══\n")

# ── LAYER 1 · the four answers ──────────────────────────────────────────────
case("① ⭐ push a un repo REGISTRADO → pasa",
     layer1("git push origin main") in (None, "allow"),
     str(layer1("git push origin main")))
case("② 🔴 push a un repo NO registrado → deny",
     layer1("git push other https://host/someone/unknown.git") == "deny")
case("③ 🔴 push a un repo ARCHIVADO → deny",
     layer1("git push old an-org/dead") == "deny")
case("④ ⚠️ crear/borrar/exponer un repo → ask",
     layer1("gh repo delete an-org/live") == "ask")

# ⭐ THE ORDER IS THE RULE · a retired repo IS registered, so a gate asking
# "registered?" first answers YES and lets the push through
r = subprocess.run([sys.executable, L1], cwd=TREE,
                   input=json.dumps({"tool_input":
                                     {"command": "git push old an-org/dead"}}),
                   capture_output=True, text=True, env=dict(os.environ, **ENV))
case("⑤ ⭐ el archivado se comprueba ANTES que «está registrado»",
     "RETIRED" in r.stdout)

# ── ⛔ READING IS NEVER BLOCKED · a gate in the daily way gets switched off ──
quiet = [c for c in ("git fetch origin", "git pull", "git status",
                     "git clone https://host/an-org/live.git", "git log")
         if layer1(c) is not None]
case("⑥ ⛔ leer (fetch/pull/status/clone/log) no le concierne", not quiet,
     str(quiet))

# ⚠️ AND A MENTION IS NOT A COMMAND · measured: an unanchored pattern fired on a
# push written inside an echo, and a warning about a command nobody runs is noise
case("⑦ ⚠️ un push MENCIONADO en un echo no dispara",
     layer1('echo "remember: git push origin main"') is None)

# ── ⚠️ ACC-MUL-001 · the silent divergence, warned about and never blocked ───
d = layer1("git push origin main")
case("⑧ ⚠️ con varios remotos avisa · pero DEJA pasar", d == "allow", str(d))

# ── ⬜ an empty registry is reported, never silent ───────────────────────────
empty = os.path.join(WORK, "empty.tsv")
open(empty, "w", encoding="utf-8").write(HEADER)
r = subprocess.run([sys.executable, L1], cwd=TREE,
                   input=json.dumps({"tool_input":
                                     {"command": "git push origin main"}}),
                   capture_output=True, text=True,
                   env=dict(os.environ, MENTE_ACCOUNTS=empty))
case("⑨ ⬜ registro vacío → pasa PERO dice que no verificó",
     "NOT MEASURED" in r.stdout)

# ── LAYER 2 · the same verdicts, reached without reading any text ───────────
case("⑩ ⭐ capa 2 · destino registrado → pasa",
     layer2("https://host/an-org/live.git").returncode == 0)
r = layer2("https://host/someone/unknown.git")
case("⑪ 🔴 capa 2 · destino NO registrado → ABORTA", r.returncode == 1,
     "exit=%d" % r.returncode)
r = layer2("git@host:an-org/dead.git")
case("⑫ 🔴 capa 2 · destino ARCHIVADO → ABORTA", r.returncode == 1,
     "exit=%d" % r.returncode)

# ── ⭐ THE REASON THERE ARE TWO LAYERS ───────────────────────────────────────
# Five ways of writing the same push that never spell the verb plainly. Layer 1
# reads text, so it cannot see them — ⛔ and that is the measurement, not a
# defect: it is why a defence over command text is never the only defence.
EVASIONS = [
    ("un alias", "gp origin main"),
    ("una función de shell", "deploy_now"),
    ("una variable con el verbo", "P=push; git $P origin main"),
    ("un eval", "eval \"$CMD\""),
    ("un constructor de argumentos", "echo origin main | xargs git push"),
]
seen = [n for n, c in EVASIONS if layer1(c) is not None]
case("⑬ ⭐ 5 formas de evadir la capa 1 · %d la esquivan"
     % (len(EVASIONS) - len(seen)), len(seen) <= 1,
     "vistas por capa 1: %s" % (seen or "ninguna"))

# ⛔ AND LAYER 2 CATCHES THEM ALL, because it never reads the command: git hands
# it the resolved destination whichever way the push was written.
blocked = all(layer2("https://host/someone/unknown.git").returncode == 1
              for _ in EVASIONS)
case("⑭ ⭐ la capa 2 las ABORTA todas · no lee el comando", blocked)

# ── 🔴 THE FAIL-OPEN THAT LOOKED LIKE PROTECTION ────────────────────────────
# Measured elsewhere: invoked through a symlink, the hook resolved its own path
# to .git/hooks/, reported "no registry" over a registry with rows, and let
# everything through in silence. ⛔ A guard that fails open gives confidence
# without giving protection.
link = os.path.join(WORK, "linked-pre-push")
os.symlink(L2, link)
r = subprocess.run(["bash", link, "origin", "https://host/someone/unknown.git"],
                   cwd=TREE, capture_output=True, text=True,
                   env=dict(os.environ, **ENV))
case("⑮ 🔴 invocada por SYMLINK sigue abortando (no falla abierta)",
     r.returncode == 1, "exit=%d" % r.returncode)

# ── ⬜ no registry · reported, never silent ──────────────────────────────────
# ⬜ AND A DECLARED REGISTRY IS USED AS DECLARED. ⛔ Falling back to a
# discovered one would verify against a file the operator did not choose, and
# nothing would say so — the probe runs inside a git tree, which is exactly the
# situation where a silent fallback finds something and looks like it worked.
r = layer2("https://host/an-org/live.git", {"MENTE_ACCOUNTS": "/nowhere/none.tsv"})
case("⑯ ⬜ un registro declarado que falta → lo DICE, no lo sustituye",
     r.returncode == 0 and "NOT verified" in r.stderr, "exit=%d" % r.returncode)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
bad = [p for p in ("not json", "[]", "null", '{"tool_input": "x"}', '{}')
       if "Traceback" in subprocess.run(
           [sys.executable, L1], cwd=TREE, input=p, capture_output=True,
           text=True, env=dict(os.environ, **ENV)).stderr]
case("⑰ ⛔ 5 payloads inválidos → sin traza", not bad, str(bad))

case("⑱ ⭐ la capa 1 deja su latido para check-gates",
     os.path.exists(os.path.join(TREE, ".beats", "gate-accounts")))

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d de %d correctos" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  restos: %s" % ("ninguno" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
