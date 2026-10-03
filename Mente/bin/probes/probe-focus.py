#!/usr/bin/env python3
"""probe-focus — does the request move the focus, and do the skills follow it?

⭐ WHAT IT MEASURES. Two hooks carry the owner's rule of 2026-10-03 (*"tu fuente de verificación es
lo que te pedí recientemente"*): `focus-signal` turns the block a request names into the FOCUS
and switches the on-demand skills; `pre-edit-standards` suggests attaching a skill when a file of
its domain is edited in a focus that has none. Both fail silently: a focus that never moves reads
exactly like a request that named no block, and a suggestion that never fires reads like a block
that needed none. Each case builds its subject — real blocks, a real registry, a real skill —
sends the hook the payload Claude Code sends, and reads the result from disk.

Runs in a throwaway tree: bin/ (the connection scripts), hooks/ (the two hooks + `_beat`),
work/blocks/, connection/. Exit: 0 every case behaves · 1 one does not
"""
import json, os, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, report                      # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-focus-")
M = os.path.join(WORK, "Mente")
FOCUS = os.path.join(M, "cache", "focus.json")
LINK = os.path.join(WORK, ".claude", "skills", "zzprobe-design")
SKILL = ("---\nname: zzprobe-design\ndescription: Design skill for the probe. Use when "
         "probing.\n---\n\nbody\n")


def case(label, ok, detail=""):
    print("  %-66s %s %s" % (label, "✅" if ok else "\U0001f534", detail))
    results.append((label, ok))


def hook(name, payload):
    r = subprocess.run([sys.executable, os.path.join(M, "hooks", name)], input=payload,
                       capture_output=True, text=True, timeout=60, cwd=WORK)
    return r.returncode, r.stdout, r.stderr


def prompt(text):
    return hook("focus-signal.py", json.dumps({"prompt": text}))


def edit(path):
    return hook("pre-edit-standards.py",
                json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}}))


def focus():
    try:
        return json.load(open(FOCUS, encoding="utf-8")).get("block")
    except (OSError, ValueError):
        return None


def block(name, state="active", skills=""):
    d = os.path.join(M, "work", "blocks", state, name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8") as fh:
        fh.write("# BLOCK · %s\n\n## ✅ IN\n- `zzprobe/%s/`\n\n## Connections\n- DEPENDS ON: "
                 "nada\n%s\n## Required standards\n- x\n" % (name, name, skills))


try:
    os.makedirs(os.path.join(M, "bin")); os.makedirs(os.path.join(M, "hooks"))
    # blockread.py: the engine's pre-edit-standards reads blocks through it
    for f in ("connection", "check-connection", "connection_lib.py", "utf8.py", "plat.py",
              "blockread.py"):
        shutil.copy2(os.path.join(ROOT, "bin", f), os.path.join(M, "bin", f))
    for f in ("focus-signal.py", "pre-edit-standards.py", "_beat.py"):
        shutil.copy2(os.path.join(ROOT, "hooks", f), os.path.join(M, "hooks", f))
    sk = os.path.join(M, "connection", "skills", "zzprobe-design")
    os.makedirs(sk)
    with open(os.path.join(sk, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(SKILL)
    sys.path.insert(0, os.path.join(ROOT, "bin"))
    import connection_lib                                  # noqa: E402
    hdr = "\n".join(connection_lib.HEADER) + "\n"   # the engine ships no registry: its header
    with open(os.path.join(M, "connection", "registry.tsv"), "w", encoding="utf-8") as fh:
        fh.write(hdr + "\t".join(["zzprobe-design", "skill", "authored:tools/x", "-", "on-demand",
                                  "2026-10-03", "MIT", "-", "none: a probe fixture, it reaches "
                                  "no account at all", "probe", "design"]) + "\n")
    block("panel-administrador-global")
    block("pilares-documentos", skills="- SKILLS: `zzprobe-design`")
    block("servidor")
    block("panel-administrador-cliente", "blocked")
    block("control-clientes", "blocked")

    rc, out, _ = prompt("vamos a trabajar en el panel de administración")
    case("① «vamos a trabajar en el panel de administración» → the ACTIVE panel",
         rc == 0 and focus() == "panel-administrador-global" and "🎯 FOCUS" in out, out[:60])
    rc, out, _ = prompt("vamos a trabajar en el panel de administración")
    case("② the same request again → silent (the focus is already there)",
         rc == 0 and out == "", repr(out[:40]))
    rc, out, _ = prompt("oye y el servidor sigue vivo?")
    case("③ a block word with NO change of topic → the focus does not move",
         rc == 0 and focus() == "panel-administrador-global" and out == "", repr(out[:40]))
    rc, out, _ = prompt("pasemos a pilares, ya contestó la clienta")
    case("④ «pasemos a pilares, ya contestó la clienta» → pilares (closest word wins)",
         focus() == "pilares-documentos", str(focus()))
    case("   … its declared skill is LINKED, and it says /reload-skills",
         os.path.isfile(os.path.join(LINK, "SKILL.md")) and "reload-skills" in out, out[-60:])
    rc, out, _ = prompt("revisa servidor y panel-administrador-global")
    case("⑤ a full hyphenated name moves it even with no phrase → the skill goes OFF",
         focus() == "panel-administrador-global" and not os.path.lexists(LINK), str(focus()))
    block("zzprobe-uno-alfa"); block("zzprobe-uno-beta")
    rc, out, _ = prompt("vamos a trabajar en zzprobe uno")
    case("⑥ two blocks match equally → NOTHING moves, and it says so",
         focus() == "panel-administrador-global" and "unchanged" in out, out[:60])
    rc, out, err = hook("focus-signal.py", "[]")
    case("⑦ a payload that is not an object → exit 0, silent", rc == 0 and out == "", str(rc))

    rc, _, err = edit(os.path.join(WORK, "zzprobe", "x", "Hero.tsx"))
    case("⑧ edit a .tsx in a focus with no design skill → 💡 ask the owner, naming the skill",
         rc == 0 and "💡 SKILL" in err and "zzprobe-design" in err, err[:60])
    rc, _, err = edit(os.path.join(WORK, "zzprobe", "x", "Other.css"))
    case("⑨ … a second UI edit in the same block → asked ONCE, not again",
         rc == 0 and "💡" not in err, err[:60])
    rc, _, err = edit(os.path.join(WORK, "zzprobe", "x", "main.py"))
    case("⑩ a file of no domain → no suggestion", "💡" not in err, err[:40])
    prompt("vamos a trabajar en pilares")
    rc, _, err = edit(os.path.join(WORK, "zzprobe", "x", "Card.tsx"))
    case("⑪ a focus that already declares a design skill → no suggestion",
         focus() == "pilares-documentos" and "💡" not in err, err[:60])
finally:
    plat.rmtree(WORK)

sys.exit(report(results))
