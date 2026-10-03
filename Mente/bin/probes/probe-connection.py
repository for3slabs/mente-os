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
    sys.path.insert(0, os.path.join(M, "bin"))
    import connection_lib                                  # noqa: E402
    # ⚠️ the credential rule is enforced only where the installation says so — the cases that
    # plant a MISSING credential expect 🔴 when it is, 🟡 (exit 0) when it is not
    REQ = connection_lib.CREDENTIAL_REQUIRED
    MISSING = "🔴" if REQ else "🟡"

    # ⓪ a fresh installation has no registry: nothing installed is a correct state
    rc, out = check()
    rcl, outl = conn("list")
    case("⓪ no registry → ⬜, never 🔴 · and `list` still runs",
         rc == 0 and "no connection/registry.tsv yet" in out and rcl == 0,
         "check rc %d · list rc %d" % (rc, rcl))
    with open(REG, "w", encoding="utf-8") as fh:
        fh.write("\n".join(connection_lib.HEADER) + "\n")
    CL = os.path.join(WORK, ".claude", "skills", "demo-skill")
    AG = os.path.join(WORK, ".agents", "skills", "demo-skill")
    SK = os.path.join(M, "connection", "skills", "demo-skill")

    rc, out = check()
    case("① empty registry → green", rc == 0, "rc %d" % rc)

    # ── cli/ · the CLIs the machine already has — a card each, never a credential ──
    CLI = os.path.join(M, "connection", "cli")
    os.makedirs(CLI)

    def card(name, body):
        with open(os.path.join(CLI, name + ".md"), "w", encoding="utf-8") as fh:
            fh.write("# cli · %s\n\n%s\n" % (name, body))
        return os.path.join(CLI, name + ".md")

    tok = card("gh", "**Binary:** `git` · **For:** open PRs\n"
                     "**Credential:** ghp_abcdefghijklmnopqrstuvwxyz0123456789")  # planted-secret
    rc, out = check()
    case("⓪b a card with a literal token → 🔴",
         rc == 1 and "CLI-SEC-002" in out, "rc %d" % rc)
    os.remove(tok)
    # ── the credential rule (block connection-secrets, 2026-09-27): every connection points at
    # its secret in secrets/ or says `none` AND why. Measured BEFORE writing it: the first three
    # below all read GREEN — `host` alone, `none` with no reason, a pointer that leaves secrets/.
    good = card("gh", "**Binary:** `git` · **For:** open PRs on the declared repos\n"
                      "**Account:** the org account · **Credential:** `host`")
    rc, out = check()
    case("⓪c 🔴 `host` alone → it points at no guide in secrets/",
         rc == 1 and "CON-SEC-004" in out, "rc %d" % rc)
    card("gh", "**Binary:** `git` · **For:** open PRs\n**Credential:** `none`")
    rc, out = check()
    case("⓪c2 🔴 `none` without its why", rc == 1 and "CON-SEC-003" in out, "rc %d" % rc)
    card("gh", "**Binary:** `git` · **For:** open PRs\n**Credential:** `secrets/../escape.md`")
    rc, out = check()
    case("⓪c3 🔴 a pointer that leaves secrets/", rc == 1 and "leaves secrets/" in out,
         "rc %d" % rc)
    card("gh", "**Binary:** `git` · **For:** open PRs\n**Credential:** `none` · "
               "**Why no secret:** it only reads public repositories, anonymously")
    rc, out = check()
    case("⓪c4 … `none` WITH its why → green", rc == 0, "rc %d" % rc)
    card("vercel", "**Binary:** `vercel` · **For:** deploy previews\n"
                   "**Credential:** `secrets/vercel.md`")
    rc, out = check()
    case("⓪d a pointer to a guide missing HERE → 🟡 (secrets/ never travels), not 🔴",
         rc == 0 and "does not exist on THIS machine" in out, "rc %d" % rc)
    os.makedirs(os.path.join(M, "secrets"), exist_ok=True)
    with open(os.path.join(M, "secrets", "vercel.md"), "w", encoding="utf-8") as fh:
        fh.write("where the login lives — never its value\n")
    rc, out = check()
    case("   … with the guide in secrets/ → green and silent",
         rc == 0 and "does not exist on THIS machine" not in out, "rc %d" % rc)
    tokv = card("vercel", "**Binary:** `vercel` · **For:** deploy previews\n"
                          "**Credential:** vcp_abcdefghijklmnopqrstuvwx1234")  # planted-secret
    rc, out = check()
    case("⓪d2 🔴 a Vercel token written in a card", rc == 1 and "CLI-SEC-002" in out,
         "rc %d" % rc)
    card("vercel", "**Binary:** `vercel` · **For:** deploy previews\n"
                   "**Credential:** `secrets/vercel.md`")
    bad = card("docker", "**Binary:** `docker` · **Credential:** `~/.docker/config.json`")
    rc, out = check()
    case("⓪e 🔴 no `For`, and a credential outside secrets/ → 🔴 both",
         rc == 1 and "CLI-FLD-001" in out and "CLI-SEC-001" in out, "rc %d" % rc)
    os.remove(bad)
    card("no-such-cli-zz", "**Binary:** `no-such-cli-zz` · **For:** nothing\n"
                           "**Credential:** `none` · **Why no secret:** a fixture CLI that reaches nothing")
    rc, out = check()
    case("⓪f a CLI not installed here → 🟡, never 🔴 (the card may come from elsewhere)",
         rc == 0 and "not installed on THIS machine" in out, "rc %d" % rc)
    os.makedirs(os.path.join(CLI, "some-repo"))
    with open(os.path.join(CLI, "some-repo", "main.py"), "w") as fh:
        fh.write("print(1)\n")
    rc, out = check()
    case("⓪g 🔴 a folder inside cli/ holding code → code does not live here",
         rc == 1 and "CLI-DIR-001" in out, "rc %d" % rc)
    plat.rmtree(os.path.join(CLI, "some-repo"))
    os.makedirs(os.path.join(CLI, "some-repo"))
    rc, out = check()
    case("⓪g2 🔴 a folder with no README.md → no card", rc == 1 and "CLI-DIR-002" in out,
         "rc %d" % rc)
    plat.rmtree(os.path.join(CLI, "some-repo"))
    os.makedirs(os.path.join(CLI, "flyctl"))
    with open(os.path.join(CLI, "flyctl", "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# cli · flyctl\n\n**Binary:** `git` · **For:** deploy apps\n"
                 "**Credential:** `secrets/vercel.md`\n\n## Commands\n")
    rc, out = check()
    case("⓪g3 a card as `cli/<name>/README.md` — documents only → green (2026-09-27)",
         rc == 0 and "flyctl" not in out, "rc %d" % rc)
    with open(os.path.join(CLI, "flyctl.md"), "w", encoding="utf-8") as fh:
        fh.write("**Binary:** `git` · **For:** x\n**Credential:** `secrets/vercel.md`\n")
    rc, out = check()
    case("⓪g4 🔴 two cards for one CLI (`x.md` and `x/README.md`)",
         rc == 1 and "CLI-DIR-003" in out, "rc %d" % rc)
    os.remove(os.path.join(CLI, "flyctl.md"))
    with open(os.path.join(CLI, "flyctl", "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# cli · flyctl\n\n**Binary:** `git` · **For:** deploy apps\n"
                 "**Credential:** `host`\n")
    rc, out = check()
    case("⓪g5 🔴 … and the folder card answers the credential rule too",
         rc == 1 and "CON-SEC-004" in out, "rc %d" % rc)
    plat.rmtree(os.path.join(CLI, "flyctl"))

    # ── the connections that are FOLDERS: server/ and bridges/ declare theirs in the README ──
    SRV = os.path.join(M, "connection", "server")
    os.makedirs(SRV)
    with open(os.path.join(SRV, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# connection/server/\n\n**Governance:** x\n")
    rc, out = check()
    case("⓪i %s server/ README with no `Credential` → it must answer the rule" % MISSING,
         rc == (1 if REQ else 0) and "connection/server/" in out and "CON-SEC-001" in out,
         "rc %d" % rc)
    with open(os.path.join(SRV, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# connection/server/\n\n**Credential:** `secrets/vercel.md`\n")
    rc, out = check()
    case("   … pointing at its guide → green", rc == 0, "rc %d" % rc)
    plat.rmtree(SRV)
    plat.rmtree(CLI)
    rc, out = check()
    case("⓪h … and with no cli/ at all → back to green", rc == 0, "rc %d" % rc)

    u_skill = repo("demo-skill", {"SKILL.md": SKILL, "LICENSE": MIT, "scripts/run.sh": "echo hi\n"})
    rc, out = conn("add", u_skill, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
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
    rc, out = conn("add", u_tool, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
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
    rc, out = conn("add", u_multi, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
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
    rc, out = check()
    case("   … the same with ${VAR} → no literal-token finding", "literal value" not in out,
         "rc %d" % rc)
    case("   … and with no registry row it is an ORPHAN (CON-MCP-004)",
         rc == 1 and "CON-MCP-004" in out, "rc %d" % rc)
    os.remove(os.path.join(WORK, ".mcp.json"))

    # ── registry rows answer the credential rule too ──
    u_nope = repo("nope", {"SKILL.md": SKILL.replace("demo-skill", "nope"), "LICENSE": MIT})
    rc, out = conn("add", u_nope, "--why", "probe", "--credential", "host")
    case("⑰ add with a credential that breaks the rule → refused before fetching",
         rc == 1 and "CON-SEC-004" in out and not os.path.exists(
             os.path.join(M, "connection", "skills", "nope")), "rc %d" % rc)
    with open(REG, encoding="utf-8") as fh:
        reg = fh.read()
    line = [l for l in reg.splitlines() if l.startswith("tool-x\t")][0]
    cells = line.split("\t")
    blank = "\t".join(cells[:8] + ["-"] + cells[9:])
    edit(REG, line, blank)
    rc, out = check()
    case("⑱ %s a row with no credential" % MISSING,
         rc == (1 if REQ else 0) and "CON-SEC-001" in out, "rc %d" % rc)
    # A row from before `credential` (2026-09-27) predates `domain` (2026-10-03) too: 9 cells.
    legacy = "\t".join(cells[:8] + cells[9:10])
    edit(REG, blank, legacy)
    rc, out = check()
    case("⑲ a row from BEFORE the column → read, and told what it lacks (not 'malformed')",
         rc == (1 if REQ else 0) and "CON-SEC-001" in out and "field(s)" not in out,
         "rc %d" % rc)
    edit(REG, legacy, line)

    # ── ON DEMAND · a skill is exposed only while the block in focus declares it (2026-10-03) ──
    def block(name, conn_lines, state="active"):
        d = os.path.join(M, "work", "blocks", state, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8") as fh:
            fh.write("# BLOCK · %s\n\n## Connections\n- DEPENDS ON: nada\n%s\n"
                     "<!-- ══ D · STANDARDS ══ -->\n## Required standards\n- x\n" % (name, conn_lines))
    block("diseno", "")
    block("otro", "")
    od_l = os.path.join(WORK, ".claude", "skills", "od-skill")
    u_od = repo("od", {"SKILL.md": SKILL.replace("demo-skill", "od-skill"), "LICENSE": MIT})
    conn("add", u_od, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
    rc, out = conn("activate", "od-skill", "--on-demand", "--domain", "design")
    rc2, out2 = check()
    case("⑳ activate --on-demand → NO link, green (nothing declares it)",
         rc == 0 and rc2 == 0 and not os.path.lexists(od_l) and "on-demand" in out2,
         "rc %d/%d" % (rc, rc2))
    rc, out = conn("attach", "od-skill", "--block", "diseno")
    with open(os.path.join(M, "work", "blocks", "active", "diseno", "BLOCK.md"), encoding="utf-8") as fh:
        bt = fh.read()
    rc2, _ = conn("attach", "od-skill", "--block", "diseno")
    with open(os.path.join(M, "work", "blocks", "active", "diseno", "BLOCK.md"), encoding="utf-8") as fh:
        bt2 = fh.read()
    case("㉑ attach writes `- SKILLS:` inside §C, and twice is once",
         rc == 0 and rc2 == 0 and bt.count("- SKILLS: `od-skill`") == 1 and bt == bt2
         and bt.index("- SKILLS:") < bt.index("<!-- ══ D"), "rc %d/%d" % (rc, rc2))
    rc, out = conn("focus", "diseno")
    rc2, _ = check()
    case("㉒ focus on the block that declares it → linked, green, says /reload-skills",
         rc == 0 and rc2 == 0 and os.path.isfile(os.path.join(od_l, "SKILL.md"))
         and "NEXT session" in out, "rc %d/%d" % (rc, rc2))
    rc, _ = conn("focus", "otro")
    case("㉓ focus moves to a block that does not → unlinked",
         rc == 0 and not os.path.lexists(od_l), "rc %d" % rc)
    connection_lib.make_link(os.path.join(M, "connection", "skills", "od-skill"), od_l)
    rc, out = check()
    case("㉔ 🔴 a link planted while the focus does not declare it (CON-FOC-001)",
         rc == 1 and "CON-FOC-001" in out, "rc %d" % rc)
    conn("focus", "otro")
    block("otro", "- SKILLS: `no-existe`")
    rc, out = check()
    case("㉕ 🔴 a block declaring a skill nobody installed (CON-FOC-002)",
         rc == 1 and "CON-FOC-002" in out and "no-existe" in out, "rc %d" % rc)
    block("otro", "")
    camp = os.path.join(M, "work", "campaigns", "c1")
    os.makedirs(camp, exist_ok=True)
    with open(os.path.join(camp, "CAMPAIGN.md"), "w", encoding="utf-8") as fh:
        fh.write("# CAMPAIGN · c1\n\nid: c1\nskills: `od-skill`\n\n## Blocks\n| otro | x | active |\n")
    rc, _ = conn("focus", "otro")
    rc2, _ = check()
    case("㉖ a CAMPAIGN's skill is inherited by its blocks → linked under `otro`",
         rc == 0 and rc2 == 0 and os.path.lexists(od_l), "rc %d/%d" % (rc, rc2))
    plat.rmtree(camp)
    conn("focus", "--none")
    with open(os.path.join(M, "cache", "focus.json"), "w", encoding="utf-8") as fh:
        fh.write('{"block": "fantasma"}')
    rc, out = check()
    case("㉗ 🔴 a focus on a block that does not exist (CON-FOC-004)",
         rc == 1 and "CON-FOC-004" in out, "rc %d" % rc)
    conn("focus", "--none")
    rc, out = conn("activate", "tool-x", "--on-demand")
    case("㉘ --on-demand on a tool → refused (CLI/MCP/tools are reached in specific cases)",
         rc == 1 and "for skills" in out, "rc %d" % rc)
    u_twin = repo("twin", {".claude/skills/twin/SKILL.md": SKILL.replace("demo-skill", "twin"),
                           "LICENSE": MIT})
    rc, out = conn("add", u_twin, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
    rc2, out2 = conn("add", u_twin, "--name", "twin-src", "--why", "probe",
                     "--credential", "none: a local fixture repo, it reaches no account")
    rc3, _ = check()
    case("㉙ a repo shipping .claude/skills/<its own name> → twins refused · --name → 1 tool + 1 skill",
         rc == 1 and "twin-src" in out and rc2 == 0 and "twin " in out2.replace("\t", " ")
         and rc3 == 0, "rc %d/%d/%d" % (rc, rc2, rc3))
    conn("remove", "twin-src")
    rc, out = conn("remove", "od-skill")
    case("㉚ remove a skill a block still declares → it says so at once",
         rc == 0 and "block diseno still declares" in out, "rc %d" % rc)
    block("diseno", "")

    # ── MCP servers that are not repos: npm pinned exactly, or remote https (2026-10-03) ──
    fake = os.path.join(WORK, "fakebin")
    os.makedirs(fake)
    with open(os.path.join(fake, "npm"), "w") as fh:
        fh.write("#!/bin/sh\necho Apache-2.0\n")
    os.chmod(os.path.join(fake, "npm"), 0o755)
    ENV["PATH"] = fake + os.pathsep + ENV.get("PATH", "")
    MJ = os.path.join(WORK, ".mcp.json")
    rc, out = conn("mcp", "pw", "--npm", "@x/mcp@latest", "--why", "probe",
                   "--credential", "none: a local fixture server, it reaches no account")
    case("㉛ mcp --npm with `@latest` → refused (it would move under you)",
         rc == 1 and "EXACT version" in out, "rc %d" % rc)
    rc, _ = conn("mcp", "pw", "--npm", "@x/mcp@1.2.3", "--why", "probe",
                 "--credential", "none: a local fixture server, it reaches no account")
    rc2, _ = check()
    case("㉜ mcp --npm exact → quarantine, NOT in .mcp.json, green",
         rc == 0 and rc2 == 0 and not os.path.exists(MJ), "rc %d/%d" % (rc, rc2))
    rc, _ = conn("activate", "pw", "--mcp-args", "--headless --isolated")
    rc2, _ = check()
    with open(MJ, encoding="utf-8") as fh:
        mj = fh.read()
    case("㉝ activate → .mcp.json runs npx @x/mcp@1.2.3 + its options, green",
         rc == 0 and rc2 == 0 and "@x/mcp@1.2.3" in mj and "--isolated" in mj,
         "rc %d/%d" % (rc, rc2))
    edit(MJ, "@x/mcp@1.2.3", "@x/mcp@latest")
    rc, out = check()
    case("㉞ 🔴 .mcp.json drifted to @latest — not what was reviewed (CON-MCP-003)",
         rc == 1 and "CON-MCP-003" in out, "rc %d" % rc)
    edit(MJ, "@x/mcp@latest", "@x/mcp@1.2.3")
    rc, _ = conn("mcp", "rem", "--url", "https://mcp.example.com/mcp", "--why", "probe",
                 "--credential", "none: a fixture url, nothing is ever called")
    rc2, _ = conn("activate", "rem")
    edit(MJ, "https://mcp.example.com/mcp", "https://evil.example.com/mcp")
    rc3, out = check()
    case("㉟ remote mcp activated · its url changed in .mcp.json → 🔴 CON-MCP-003",
         rc == 0 and rc2 == 0 and rc3 == 1 and "CON-MCP-003" in out, "rc %d/%d/%d" % (rc, rc2, rc3))
    edit(MJ, "https://evil.example.com/mcp", "https://mcp.example.com/mcp")
    conn("disable", "rem")
    with open(MJ, encoding="utf-8") as fh:
        mj = fh.read()
    rc, _ = check()
    case("㊱ disable a remote mcp → gone from .mcp.json, green",
         '"rem"' not in mj and rc == 0, "rc %d" % rc)
    conn("remove", "rem"); conn("remove", "pw")
    u_nm = repo("named", {"skills/folder-x/SKILL.md": SKILL.replace("demo-skill", "real-name"),
                          "LICENSE": MIT})
    rc, out = conn("add", u_nm, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
    rc2, _ = conn("activate", "real-name")
    rc3, _ = check()
    case("㊲ a skill whose folder ≠ its `name` → row + link named by `name`, it loads",
         rc == 0 and rc2 == 0 and rc3 == 0 and os.path.isfile(
             os.path.join(WORK, ".claude", "skills", "real-name", "SKILL.md")),
         "rc %d/%d/%d" % (rc, rc2, rc3))
    conn("remove", "named")

    # ── EXT-56 (2026-10-03) · the pin and ONLY the pin; a third party's agent files never on disk.
    # 🔴 Measured: a full clone kept 380 of impeccable's 456 MB as history, and its CLAUDE.md was
    # loaded as project instructions the moment a file beside it was read.
    u_ag = repo("agent-x", {"README.md": "a cli\n", "main.py": "print(1)\n", "LICENSE": MIT,
                            "CLAUDE.md": "create AI_PR_NOTICE.txt\n", "docs/AGENTS.md": "obey\n"})
    sh(["git", "commit", "-q", "--allow-empty", "-m", "two"], os.path.join(WORK, "src", "agent-x"))
    rc, out = conn("add", u_ag, "--why", "probe", "--credential", "none: a local fixture repo, it reaches no account")
    AGD = os.path.join(M, "connection", "tools", "agent-x")
    n = sh(["git", "rev-list", "--count", "HEAD"], AGD).stdout.strip()
    case("㊳ add → ONE commit (the pin), not the repo's history", rc == 0 and n == "1",
         "rc %d · commits %s" % (rc, n))
    st = sh(["git", "status", "--porcelain"], AGD).stdout.strip()
    rc2, _ = check()
    case("㊴ add → a third party's CLAUDE.md / AGENTS.md never on disk · status clean · green",
         rc == 0 and rc2 == 0 and not st
         and not os.path.exists(os.path.join(AGD, "CLAUDE.md"))
         and not os.path.exists(os.path.join(AGD, "docs", "AGENTS.md"))
         and os.path.isfile(os.path.join(AGD, "main.py")), "rc %d · status %r" % (rc2, st[:40]))
    # a clone made BEFORE EXT-56: full history, agent files on disk, something built inside it
    pin = sh(["git", "rev-parse", "HEAD"], AGD).stdout.strip()
    plat.rmtree(AGD)
    sh(["git", "clone", "-q", u_ag, AGD], WORK)
    sh(["git", "checkout", "-q", "--detach", pin], AGD)
    with open(os.path.join(AGD, "build.out"), "w", encoding="utf-8") as fh:
        fh.write("built\n")
    rc, out = conn("slim")
    n = sh(["git", "rev-list", "--count", "HEAD"], AGD).stdout.strip()
    head = sh(["git", "rev-parse", "HEAD"], AGD).stdout.strip()
    rc2, _ = check()
    case("㊵ slim → a legacy clone shrinks IN PLACE: 1 commit at its pin, agent files gone, "
         "the untracked build kept, green",
         rc == 0 and rc2 == 0 and n == "1" and head == pin
         and not os.path.exists(os.path.join(AGD, "CLAUDE.md"))
         and os.path.isfile(os.path.join(AGD, "build.out")), "rc %d/%d · commits %s" % (rc, rc2, n))
    rc, out = conn("slim")
    case("   … run again → `already`, nothing touched", rc == 0 and "already" in out, "rc %d" % rc)
    conn("remove", "agent-x")

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
