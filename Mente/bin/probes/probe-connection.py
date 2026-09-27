#!/usr/bin/env python3
"""probe-connection — does the installer do the one path, and does the checker catch each defect?

⭐ WHAT IT MEASURES. `bin/connection` installs third-party code an agent will
obey; `bin/check-connection` is the only thing that says it was done right.
Both can fail silently: the installer exposing before review, the checker
staying green over a skill that will never load. Each case builds its subject
— real git repos as sources, a real registry, real links — and plants ONE
defect whose right answer is known. A checker that stays green on a planted
defect is reported red here.

Runs in a throwaway tree: bin/ (only the three scripts it needs), connection/,
.gitignore, inside a fresh `git init` so ignore rules are real.

Exit: 0 every case behaves · 1 one does not
"""
import os, shutil, subprocess, sys, tempfile
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
WORK = tempfile.mkdtemp(prefix="mente-conn-")
M = os.path.join(WORK, "Mente")
ENV = dict(os.environ, GIT_AUTHOR_NAME="p", GIT_AUTHOR_EMAIL="p@p",
           GIT_COMMITTER_NAME="p", GIT_COMMITTER_EMAIL="p@p")


def case(label, ok, detail=""):
    print("  %-62s %s %s" % (label, "✅" if ok else "\U0001f534", detail))
    results.append((label, ok))


def sh(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=ENV, timeout=120)


def conn(*args):
    r = sh([sys.executable, os.path.join(M, "bin", "connection")] + list(args), WORK)
    return r.returncode, r.stdout + r.stderr


def check():
    r = sh([sys.executable, os.path.join(M, "bin", "check-connection")], WORK)
    return r.returncode, r.stdout + r.stderr


def repo(name, files):
    p = os.path.join(WORK, "src", name)
    for rel, body in files.items():
        f = os.path.join(p, rel)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(body)
    sh(["git", "init", "-q"], p); sh(["git", "add", "-A"], p)
    sh(["git", "commit", "-q", "-m", "init"], p)
    return "file://" + p


def edit(path, old, new):
    with open(path, encoding="utf-8") as fh:
        t = fh.read()
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(t.replace(old, new, 1))


SKILL = "---\nname: demo-skill\ndescription: Demo skill for the probe. Use when probing.\n---\n\nbody\n"
MIT = "MIT License\n\nPermission is hereby granted, free of charge, to any person\n"

try:
    os.makedirs(os.path.join(M, "bin"))
    for f in ("connection", "check-connection", "connection_lib.py", "utf8.py", "plat.py"):
        shutil.copy2(os.path.join(ROOT, "bin", f), os.path.join(M, "bin", f))
    os.makedirs(os.path.join(M, "connection"))
    shutil.copy2(os.path.join(ROOT, "connection", "README.md"),
                 os.path.join(M, "connection", "README.md"))
    shutil.copy2(os.path.join(ROOT, ".gitignore"), os.path.join(M, ".gitignore"))
    sh(["git", "init", "-q"], WORK)
    REG = os.path.join(M, "connection", "registry.tsv")

    # ⓪ a fresh installation has no registry: nothing installed is a correct state
    rc, out = check()
    rcl, outl = conn("list")
    case("⓪ no registry → ⬜, never 🔴 · and `list` still runs",
         rc == 0 and "no connection/registry.tsv yet" in out and rcl == 0,
         "check rc %d · list rc %d" % (rc, rcl))

    # ── cli/ · the CLIs the machine already has — a card each, never a credential ──
    CLI = os.path.join(M, "connection", "cli")
    os.makedirs(CLI)

    def card(name, body):
        with open(os.path.join(CLI, name + ".md"), "w", encoding="utf-8") as fh:
            fh.write("# cli · %s\n\n%s\n" % (name, body))
        return os.path.join(CLI, name + ".md")

    # 🔴 THE HOLE THIS CLOSES: with no registry, the checker used to return green
    # BEFORE looking at anything else — a card carrying a token would pass there.
    tok = card("gh", "**Binary:** `git` · **For:** open PRs\n"
                     "**Credential:** ghp_abcdefghijklmnopqrstuvwxyz0123456789")  # planted-secret
    rc, out = check()
    case("⓪b no registry + a card with a literal token → 🔴, not ⬜",
         rc == 1 and "CLI-SEC-002" in out, "rc %d" % rc)
    os.remove(tok)
    good = card("gh", "**Binary:** `git` · **For:** open PRs on the declared repos\n"
                      "**Account:** the org account · **Credential:** `host`")
    rc, out = check()
    case("⓪c … the same card pointing at `host` → green", rc == 0, "rc %d" % rc)
    card("vercel", "**Binary:** `vercel` · **For:** deploy previews\n"
                   "**Credential:** `secrets/vercel.md`")
    rc, out = check()
    case("⓪d a card pointing into secrets/ → green", rc == 0, "rc %d" % rc)
    bad = card("docker", "**Binary:** `docker` · **Credential:** `~/.docker/config.json`")
    rc, out = check()
    case("⓪e 🔴 no `For`, and a credential outside secrets/ → 🔴 both",
         rc == 1 and "CLI-FLD-001" in out and "CLI-SEC-001" in out, "rc %d" % rc)
    os.remove(bad)
    card("no-such-cli-zz", "**Binary:** `no-such-cli-zz` · **For:** nothing\n**Credential:** `none`")
    rc, out = check()
    case("⓪f a CLI not installed here → 🟡, never 🔴 (the card may come from elsewhere)",
         rc == 0 and "not installed on THIS machine" in out, "rc %d" % rc)
    os.makedirs(os.path.join(CLI, "some-repo"))
    rc, out = check()
    case("⓪g 🔴 a folder inside cli/ → code does not live here",
         rc == 1 and "CLI-DIR-001" in out, "rc %d" % rc)
    plat.rmtree(CLI)
    rc, out = check()
    case("⓪h … and with no cli/ at all → back to ⬜", rc == 0, "rc %d" % rc)
    sys.path.insert(0, os.path.join(M, "bin"))
    import connection_lib                                  # noqa: E402
    with open(REG, "w", encoding="utf-8") as fh:
        fh.write("\n".join(connection_lib.HEADER) + "\n")
    CL = os.path.join(WORK, ".claude", "skills", "demo-skill")
    AG = os.path.join(WORK, ".agents", "skills", "demo-skill")
    SK = os.path.join(M, "connection", "skills", "demo-skill")

    rc, out = check()
    case("① empty registry → green", rc == 0, "rc %d" % rc)

    u_skill = repo("demo-skill", {"SKILL.md": SKILL, "LICENSE": MIT, "scripts/run.sh": "echo hi\n"})
    rc, out = conn("add", u_skill, "--why", "probe")
    rc2, _ = check()
    case("② add → quarantine, NOT exposed, checker green",
         rc == 0 and "quarantine" in out and not os.path.lexists(CL) and rc2 == 0,
         "rc %d/%d" % (rc, rc2))
    case("   … review list names SKILL.md and the script",
         "SKILL.md" in out and "scripts/run.sh" in out, "")
    case("   … license read from its LICENSE", "license MIT" in out, "")

    os.makedirs(os.path.dirname(CL), exist_ok=True)
    connection_lib.make_link(SK, CL)
    rc, out = check()
    case("③ quarantine with a link planted → 🔴", rc == 1 and "before review" in out,
         "rc %d" % rc)
    connection_lib.drop_link(CL)

    rc, out = conn("activate", "demo-skill")
    rc2, _ = check()
    case("④ activate → both links resolve to the real folder, green",
         rc == 0 and os.path.realpath(CL) == os.path.realpath(SK)
         and os.path.realpath(AG) == os.path.realpath(SK) and rc2 == 0,
         "rc %d/%d" % (rc, rc2))
    case("   … it warns the skill is seen from the NEXT session", "NEXT session" in out, "")

    edit(os.path.join(SK, "SKILL.md"), "name: demo-skill", "name: other-name")
    rc, out = check()
    case("⑤ name ≠ folder → 🔴 (it would never load)", rc == 1 and "will not load" in out,
         "rc %d" % rc)
    edit(os.path.join(SK, "SKILL.md"), "name: other-name", "name: demo-skill")

    edit(os.path.join(SK, "SKILL.md"), "---\nname", "\n---\nname")
    rc, out = check()
    case("⑥ line 1 is not `---` → 🔴", rc == 1 and "line 1" in out, "rc %d" % rc)
    edit(os.path.join(SK, "SKILL.md"), "\n---\nname", "---\nname")

    with open(os.path.join(SK, "extra.txt"), "w") as fh:
        fh.write("x")
    sh(["git", "add", "-A"], SK); sh(["git", "commit", "-q", "-m", "drift"], SK)
    rc, out = check()
    case("⑦ clone moved off its pinned sha → 🔴", rc == 1 and "drifted" in out, "rc %d" % rc)
    sh(["git", "reset", "-q", "--hard", "HEAD~1"], SK)

    os.makedirs(os.path.join(M, "connection", "skills", "stray"))
    rc, out = check()
    case("⑧ a folder with no registry row → 🔴", rc == 1 and "no registry row" in out,
         "rc %d" % rc)
    os.rmdir(os.path.join(M, "connection", "skills", "stray"))

    with open(REG, encoding="utf-8") as fh:
        reg = fh.read()
    sha = [l for l in reg.splitlines() if l.startswith("demo-skill\t")][0].split("\t")[3]
    edit(REG, sha, "main")
    rc, out = check()
    case("⑨ ref is a branch, not a sha → 🔴", rc == 1 and "full sha" in out, "rc %d" % rc)
    edit(REG, "\tmain\t", "\t%s\t" % sha)

    connection_lib.drop_link(CL)
    rc, out = check()
    rc2, _ = conn("sync")
    rc3, _ = check()
    case("⑩ active skill lost its link → 🔴 · sync re-makes it → green",
         rc == 1 and rc2 == 0 and rc3 == 0 and connection_lib.is_link(CL), "rc %d/%d/%d" % (rc, rc2, rc3))

    u_tool = repo("tool-x", {"README.md": "a cli\n", "main.py": "print(1)\n", "LICENSE": MIT})
    rc, out = conn("add", u_tool, "--why", "probe")
    case("⑪ a repo with no SKILL.md → tools/, and it says to author one",
         rc == 0 and os.path.isdir(os.path.join(M, "connection", "tools", "tool-x"))
         and "author" in out, "rc %d" % rc)
    rc, out = conn("author", "tool-x", "drive-x", "--description", "Drives tool-x. Use when x.")
    tracked = sh(["git", "ls-files", "--error-unmatch",
                  "Mente/connection/skills/drive-x/SKILL.md"], WORK).returncode == 0
    case("   … author writes the SKILL.md and VERSIONS it (git add -f)",
         rc == 0 and tracked, "rc %d" % rc)
    rc, out = conn("activate", "drive-x")
    case("   … activate refuses while the ⬜ placeholder is there", rc == 1, "rc %d" % rc)
    edit(os.path.join(M, "connection", "skills", "drive-x", "SKILL.md"),
         "## ⬜ How to use it", "## How to use it")
    rc, _ = conn("activate", "drive-x")
    rc2, out2 = check()
    case("   … once written, activate + checker green", rc == 0 and rc2 == 0,
         "rc %d/%d" % (rc, rc2))
    # -f: the SKILL.md was edited after `add`, and a plain `rm --cached` REFUSES — the
    # sabotage silently did not happen and ⑫ read green on an untouched tree (caught 2026-09-26)
    _r = sh(["git", "rm", "-q", "-f", "--cached", "Mente/connection/skills/drive-x/SKILL.md"], WORK)
    assert _r.returncode == 0, "the sabotage itself failed: " + _r.stderr
    rc, out = check()
    case("⑫ authored skill NOT versioned → 🔴 (the only copy)",
         rc == 1 and "only copy" in out, "rc %d" % rc)
    sh(["git", "add", "-f", "Mente/connection/skills/drive-x/SKILL.md"], WORK)

    u_multi = repo("multi", {"skills/a-one/SKILL.md": SKILL.replace("demo-skill", "a-one"),
                             "skills/b-two/SKILL.md": SKILL.replace("demo-skill", "b-two")})
    rc, out = conn("add", u_multi, "--why", "probe")
    rc2, _ = conn("activate", "a-one")
    rc3, _ = check()
    a1 = os.path.join(WORK, ".claude", "skills", "a-one")
    case("⑬ a repo shipping skills/*/SKILL.md → 1 tool + 2 skill rows, each linkable",
         rc == 0 and "a-one" in out and "b-two" in out and rc2 == 0 and rc3 == 0
         and os.path.isfile(os.path.join(a1, "SKILL.md")), "rc %d/%d/%d" % (rc, rc2, rc3))

    with open(os.path.join(WORK, ".mcp.json"), "w") as fh:
        fh.write('{"mcpServers":{"x":{"type":"http","url":"https://x",'
                 '"headers":{"Authorization":"Bearer sk_live_abcdefghijklmnop1234"}}}}')
    rc, out = check()
    case("⑭ .mcp.json with a literal token → 🔴", rc == 1 and "literal value" in out,
         "rc %d" % rc)
    with open(os.path.join(WORK, ".mcp.json"), "w") as fh:
        fh.write('{"mcpServers":{"x":{"type":"http","url":"https://x",'
                 '"headers":{"Authorization":"Bearer ${X_TOKEN}"}}}}')
    rc, _ = check()
    case("   … the same with ${VAR} → green", rc == 0, "rc %d" % rc)

    plat.rmtree(os.path.join(M, "connection", "tools", "tool-x"))
    rc, out = check()
    rc2, _ = conn("sync")
    rc3, _ = check()
    case("⑮ fresh clone (code missing) → 🟡 not 🔴 · sync restores at the pin",
         rc == 0 and "sync" in out and rc2 == 0 and rc3 == 0
         and os.path.isfile(os.path.join(M, "connection", "tools", "tool-x", "main.py")),
         "rc %d/%d/%d" % (rc, rc2, rc3))

    rc, _ = conn("remove", "demo-skill")
    rc2, _ = check()
    with open(REG, encoding="utf-8") as fh:
        still = "demo-skill\t" in fh.read()
    case("⑯ remove → folder, both links and the row gone, green",
         rc == 0 and rc2 == 0 and not os.path.exists(SK) and not os.path.lexists(CL)
         and not os.path.lexists(AG) and not still, "rc %d/%d" % (rc, rc2))
finally:
    plat.rmtree(WORK)

sys.exit(report(results))
