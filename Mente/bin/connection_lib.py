"""connection_lib — the ONE implementation of what connection/ means.

⭐ Read by `bin/connection` (the installer) and `bin/check-connection` (the
verifier). Two scripts that each carried their own copy of "what a valid skill
is" would drift, and the verifier would bless what the installer never wrote —
the same reason Maestro kept its logic in a single `maestro_lib.sh`.

What lives here: the registry format · where a row's content lives · the Agent
Skills rules (agentskills.io/specification, read 2026-09-26) · the link paths.
⛔ No third-party YAML parser: the engine runs on a bare Python, so the
frontmatter reader below handles the subset a SKILL.md uses and says so when
it meets something it cannot read.
"""
import os
import re
import subprocess
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(MENTE)
CONN = os.path.join(MENTE, "connection")
REGISTRY = os.path.join(CONN, "registry.tsv")
# ⭐ A fresh installation has NO registry: nothing third-party was installed yet.
# That is a correct state, not a broken one — so a missing file reads as an empty
# registry, and the first write creates it with this header.
HEADER = [
    "# registry.tsv — every third-party component this installation carries. ONE row per component.",
    "# ⭐ The lockfile of connection/: the CONTENT of a third-party component is gitignored and",
    "#    `bin/connection sync` restores it from here. What git keeps is this file — never the code.",
    "# ⚠️ Instance data, versioned on purpose with `git add -f`: without the row a fresh clone",
    "#    cannot know what to restore, and nothing could verify it.",
    "#",
    "# Format (TAB-separated): name  type  source  ref  state  installed  license  exposes  credential  why  domain",
    "#   name      = folder name under <type>/ · [a-z0-9-], 1-64, no leading/trailing/double hyphen",
    "#   type      = skill | mcp | tool",
    "#   source    = git URL · \"authored:<path>\" when WE wrote it (a SKILL.md for a repo that had none)",
    "#   ref       = the full commit sha it is pinned to · \"-\" only for authored",
    "#   state     = quarantine (fetched, not reviewed, NOT exposed) · active · on-demand · disabled",
    "#               on-demand = reviewed, linked ONLY while the block in focus declares it",
    "#   installed = YYYY-MM-DD",
    "#   license   = SPDX id read from the component's LICENSE · \"unknown\" is a finding, not a value",
    "#   exposes   = where the agent sees it, comma-separated, from the project root:",
    "#               .claude/skills/<name> · .agents/skills/<name> · .mcp.json:<name> · \"-\"",
    "#   credential= WHERE its access lives: `secrets/<file>` · or `none: <why it needs no secret>`",
    "#               (see CREDENTIAL_REQUIRED in bin/connection_lib.py)",
    "#   why       = who asked and for what, one line",
    "#   domain    = what kind of work an on-demand skill serves (design …) · \"-\"",
    "#",
    "# Written by: bin/connection (never by hand). Verified by: bin/check-connection.",
]

FIELDS = ["name", "type", "source", "ref", "state", "installed", "license",
          "exposes", "why"]
TYPES = {"skill": "skills", "mcp": "mcp", "tool": "tools"}
STATES = ("quarantine", "active", "disabled")
# Where each agent looks for project skills — both follow a symlinked folder
# (their docs, 2026-09-26; measured for Claude Code the same day).
SKILL_HOMES = (".claude/skills", ".agents/skills")


# 🔴 WINDOWS REFUSES A SYMLINK TO A NORMAL ACCOUNT. Measured 2026-09-27 on a native
# install: `os.symlink` → WinError 1314, and `activate` died before exposing anything.
# ⭐ A directory JUNCTION needs no privilege and every agent follows it like a link —
# the same fallback bin/init uses for git hooks. These three are the only way a skill
# link is made, recognised or removed, so the checker and the command never disagree.
def is_link(p):
    """A symlink, or — on Windows — the junction make_link falls back to."""
    return os.path.islink(p) or bool(getattr(os.path, "isjunction", lambda _p: False)(p))


def make_link(target, p):
    try:
        os.symlink(os.path.relpath(target, os.path.dirname(p)), p)
    except OSError:
        if os.name != "nt":
            raise
        import _winapi
        _winapi.CreateJunction(os.path.abspath(target), p)


def drop_link(p):
    """Remove the link, never what it points at."""
    if os.path.islink(p):
        os.unlink(p)
    else:
        os.rmdir(p)     # a junction: rmdir removes the link, the target stays

# ── cli/ · the CLIs ALREADY INSTALLED on this machine that the agent works with ──
# ⭐ Not code: `tools/` holds a fetched repo, `cli/` holds a CARD per CLI the machine already
# has (`gh`, `vercel`, `docker`…) — what the agent uses it for, with which account, and WHERE
# its credential lives. ⛔ Never the credential itself: that is `secrets/`, or the CLI's own
# login store (`host`). A card is instance data, versioned by `bin/init`'s keep-block.
CLI_DIR = os.path.join(CONN, "cli")
CLI_FIELDS = ("Binary", "For", "Account", "Credential")
CLI_REQUIRED = ("Binary", "For", "Credential")
CLI_CRED_WORDS = ("none", "host")
_CARD_FIELD = re.compile(r"\*\*(%s):\*\*\s*(.+?)(?=\s+·\s+\*\*|$)" % "|".join(CLI_FIELDS))
# A value that LOOKS like a credential: a known token prefix, or a long mixed run.
_TOKENISH = re.compile(r"(ghp_|gho_|ghs_|github_pat_|glpat-|sk-|sk_live_|rk_live_|xox[abpr]-|"
                       r"AKIA[0-9A-Z]{12,}|eyJ[A-Za-z0-9_-]{10,}\.)|"
                       r"\b(?=[A-Za-z0-9_\-]*\d)(?=[A-Za-z0-9_\-]*[A-Za-z])[A-Za-z0-9_\-]{32,}\b")


def read_card(path):
    """A CLI card → {field: value}, values with their backticks stripped."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            for k, v in _CARD_FIELD.findall(line.strip()):
                out.setdefault(k, v.strip().strip("`").strip())
    return out


def cli_findings(which=None):
    """Every card in cli/ against the rules → [(level, who, message)], level 'red'|'yellow'.

    ⭐ Independent of the registry: a card declares a CLI the machine already has, so a
    fresh install with no registry still has its cards checked."""
    import shutil
    which = which or shutil.which
    found = []
    if not os.path.isdir(CLI_DIR):
        return found
    for entry in sorted(os.listdir(CLI_DIR)):
        p = os.path.join(CLI_DIR, entry)
        who = "cli/%s" % entry
        if os.path.isdir(p):
            found.append(("red", who, "a folder in cli/ — code does not live here; a fetched "
                                      "repo belongs to ../tools/ (CLI-DIR-001)"))
            continue
        if entry == "README.md" or not entry.endswith(".md"):
            continue
        name = entry[:-3]
        if not valid_name(name):
            found.append(("red", who, "card name must be [a-z0-9-] like its CLI (CLI-NAM-001)"))
        card = read_card(p)
        missing = [f for f in CLI_REQUIRED if not card.get(f)]
        if missing:
            found.append(("red", who, "missing %s — a card says what the CLI is for and where "
                                      "its credential lives (CLI-FLD-001)" % ", ".join(missing)))
        cred = card.get("Credential", "")
        if cred and cred.lower() not in CLI_CRED_WORDS and not cred.startswith("secrets/"):
            found.append(("red", who, "Credential must be `secrets/<file>`, `host` or `none` — "
                                      "got %r (CLI-SEC-001)" % cred[:40]))
        text = open(p, encoding="utf-8").read()
        hit = _TOKENISH.search(text)
        if hit:
            found.append(("red", who, "something that looks like a credential is written here "
                                      "(%s…) — it belongs in secrets/ (CLI-SEC-002)" % hit.group(0)[:6]))
        binary = card.get("Binary", "")
        if binary and not which(binary):
            found.append(("yellow", who, "`%s` is not installed on THIS machine — the card may "
                                         "come from another one" % binary))
    return found


FIELDS = ["name", "type", "source", "ref", "state", "installed", "license",
          "exposes", "credential", "why", "domain"]
TYPES = {"skill": "skills", "mcp": "mcp", "tool": "tools"}
# ⭐ `on-demand` (2026-10-03): reviewed and on disk, but linked ONLY while the block in
# focus declares it. *"no pueden estar siempre activas todas, eso consumiría demasiados tokens por
# procesos que no estamos realizando"* — every exposed skill puts its description in EVERY turn.
STATES = ("quarantine", "active", "on-demand", "disabled")
# Where each agent looks for project skills — both follow a symlinked folder
# (their docs, 2026-09-26; measured for Claude Code the same day).
SKILL_HOMES = (".claude/skills", ".agents/skills")
# Where a REPO ships its skills, in the order `add` looks — `skills/` is the portable layout.
INNER_SKILL_HOMES = ("skills", ".claude/skills")


# 🔴 WINDOWS REFUSES A SYMLINK TO A NORMAL ACCOUNT. Measured 2026-09-27 on a native
# install: `os.symlink` → WinError 1314, and `activate` died before exposing anything.
# ⭐ A directory JUNCTION needs no privilege and every agent follows it like a link —
# the same fallback bin/init uses for git hooks. These three are the only way a skill
# link is made, recognised or removed, so the checker and the command never disagree.
def is_link(p):
    """A symlink, or — on Windows — the junction make_link falls back to."""
    return os.path.islink(p) or bool(getattr(os.path, "isjunction", lambda _p: False)(p))


def make_link(target, p):
    try:
        os.symlink(os.path.relpath(target, os.path.dirname(p)), p)
    except OSError:
        if os.name != "nt":
            raise
        import _winapi
        _winapi.CreateJunction(os.path.abspath(target), p)


def drop_link(p):
    """Remove the link, never what it points at."""
    if os.path.islink(p):
        os.unlink(p)
    else:
        os.rmdir(p)     # a junction: rmdir removes the link, the target stays

# ── the credential rule · EVERY connection answers it (block connection-secrets) ──
# ⭐ The owner, 2026-09-27: *"cuando exista una connection debe de estar relacionada con un
# secrets; si no es así, argumenta el por qué"*. A connection points at its secret —
# `secrets/<file>`, the guide that says WHERE the access lives and how it is rotated — or it
# says `none` AND why. ⛔ `host` alone is gone: a CLI's own login store (`auth.json`, a
# keyring) is a secret too, and its guide in secrets/ is what says where it is.
# Measured before writing: `host`, `none` without a reason and `secrets/../x` all passed.
# ⚠️ CREDENTIAL_REQUIRED · False in the engine (2026-10-03): the registry carries the
# `credential` column, but a connection that declares NONE is 🟡, not 🔴 — an installation
# made before the column would otherwise turn red on update. A credential that IS declared
# is still checked in full (`host` alone, `none` without its why, a path leaving secrets/).
# An owner who wants the rule enforced sets it to True.
CREDENTIAL_REQUIRED = False
SECRETS_DIR = os.path.join(MENTE, "secrets")
WHY_MIN = 20            # a reason, not a word — "n/a" is not an argument


def credential_findings(cred, why, who):
    """→ [(level, who, message)] for ONE connection's credential declaration."""
    c = (cred or "").strip().strip("`").strip()
    if not c:
        return [("red" if CREDENTIAL_REQUIRED else "yellow", who,
                 "no credential declared — `secrets/<file>`, or `none` and why (CON-SEC-001)")]
    if c.lower() == "none":
        if len((why or "").strip()) < WHY_MIN:
            return [("red", who, "`none` without its why — say why this connection needs no "
                                 "secret, it is then weighed and decided (CON-SEC-003)")]
        return []
    if c.lower() == "host":
        return [("red", who, "`host` alone points nowhere — write the guide in secrets/ that "
                             "says where the CLI keeps its login and how to rotate it, and "
                             "point at it (CON-SEC-004)")]
    if not c.startswith("secrets/"):
        return [("red", who, "credential must be `secrets/<file>` or `none` — got %r "
                             "(CLI-SEC-001)" % c[:40])]
    rel = c[len("secrets/"):]
    parts = rel.replace("\\", "/").split("/")
    if not rel or ".." in parts or os.path.isabs(rel):
        return [("red", who, "`%s` leaves secrets/ (CLI-SEC-001)" % c[:40])]
    if not os.path.isfile(os.path.join(SECRETS_DIR, rel)):
        # 🟡, not 🔴: secrets/ never travels — a fresh clone has the pointer, not the guide.
        return [("yellow", who, "`%s` does not exist on THIS machine — secrets/ never "
                                "travels; write the guide here" % c)]
    return []


# ── cli/ · the CLIs ALREADY INSTALLED on this machine that the agent works with ──
# ⭐ Not code: `tools/` holds a fetched repo, `cli/` holds a CARD per CLI the machine already
# has (`gh`, `vercel`, `docker`…) — what the agent uses it for, with which account, and WHERE
# its credential lives. ⛔ Never the credential itself: that is `secrets/`. A card is
# `cli/<name>.md`, or `cli/<name>/README.md` when it is a full manual (2026-09-27) —
# a folder of DOCUMENTS only: code would be code nobody reviewed (CLI-DIR-001).
# A card is instance data, versioned by `bin/init`'s keep-block.
CLI_DIR = os.path.join(CONN, "cli")
CLI_FIELDS = ("Binary", "For", "Account", "Credential", "Why no secret")
CLI_REQUIRED = ("Binary", "For", "Credential")
_CARD_FIELD = re.compile(r"\*\*(%s):\*\*\s*(.+?)(?=\s+·\s+\*\*|$)" % "|".join(CLI_FIELDS))
# A value that LOOKS like a credential: a known token prefix, or a long mixed run.
_TOKENISH = re.compile(r"(ghp_|gho_|ghs_|github_pat_|glpat-|sk-|sk_live_|rk_live_|xox[abpr]-|"
                       r"\bvc[a-z]_[A-Za-z0-9]{20,}|"
                       r"AKIA[0-9A-Z]{12,}|eyJ[A-Za-z0-9_-]{10,}\.)|"
                       r"\b(?=[A-Za-z0-9_\-]*\d)(?=[A-Za-z0-9_\-]*[A-Za-z])[A-Za-z0-9_\-]{32,}\b")


def row_credential(row):
    """A registry row's `credential` → (pointer, why): `secrets/<file>` · `none: <why>`."""
    v = (row.get("credential") or "").strip()
    if v.lower().startswith("none"):
        return "none", v[4:].lstrip(" :—-")
    return ("" if v == "-" else v), ""


# ── the connections that are FOLDERS, not rows: their README declares the credential ──
FOLDER_CONNECTIONS = ("server", "bridges")


def folder_findings():
    """`server/` and `bridges/` reach outside too: each README carries `**Credential:**`."""
    found = []
    for sub in FOLDER_CONNECTIONS:
        who = "connection/%s/" % sub
        p = os.path.join(CONN, sub, "README.md")
        if not os.path.isfile(p):
            # ⛔ said out loud, never a silent pass (CHK-CAU-003)
            found.append(("yellow", who, "no README.md — its credential NOT checked"))
            continue
        card = read_card(p)
        found += credential_findings(card.get("Credential", ""), card.get("Why no secret", ""),
                                     who)
    return found


def read_card(path):
    """A CLI card → {field: value}, values with their backticks stripped."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            for k, v in _CARD_FIELD.findall(line.strip()):
                out.setdefault(k, v.strip().strip("`").strip())
    return out


def cli_findings(which=None):
    """Every card in cli/ against the rules → [(level, who, message)], level 'red'|'yellow'.

    ⭐ Independent of the registry: a card declares a CLI the machine already has, so a
    fresh install with no registry still has its cards checked."""
    import shutil
    which = which or shutil.which
    found = []
    if not os.path.isdir(CLI_DIR):
        return found
    for entry in sorted(os.listdir(CLI_DIR)):
        p = os.path.join(CLI_DIR, entry)
        who = "cli/%s" % entry
        if os.path.isdir(p):
            who += "/"
            extra = sorted(f for f in os.listdir(p)
                           if os.path.isdir(os.path.join(p, f)) or not f.endswith(".md"))
            if extra:
                found.append(("red", who, "holds %s — only a card's documents (.md) live in "
                                          "cli/; a fetched repo belongs to ../tools/ "
                                          "(CLI-DIR-001)" % ", ".join(extra[:3])))
                continue
            if not os.path.isfile(os.path.join(p, "README.md")):
                found.append(("red", who, "a folder with no README.md — its card is "
                                          "`cli/%s/README.md` (CLI-DIR-002)" % entry))
                continue
            if os.path.isfile(p + ".md"):
                found.append(("red", who, "two cards for one CLI — `%s.md` and `%s/README.md` "
                                          "(CLI-DIR-003)" % (entry, entry)))
            name, p = entry, os.path.join(p, "README.md")
        elif entry == "README.md" or not entry.endswith(".md"):
            continue
        else:
            name = entry[:-3]
        if not valid_name(name):
            found.append(("red", who, "card name must be [a-z0-9-] like its CLI (CLI-NAM-001)"))
        card = read_card(p)
        missing = [f for f in CLI_REQUIRED if not card.get(f)]
        if missing:
            found.append(("red", who, "missing %s — a card says what the CLI is for and where "
                                      "its credential lives (CLI-FLD-001)" % ", ".join(missing)))
        if card.get("Credential"):
            found += credential_findings(card["Credential"], card.get("Why no secret", ""), who)
        text = open(p, encoding="utf-8").read()
        hit = _TOKENISH.search(text)
        if hit:
            found.append(("red", who, "something that looks like a credential is written here "
                                      "(%s…) — it belongs in secrets/ (CLI-SEC-002)" % hit.group(0)[:6]))
        binary = card.get("Binary", "")
        if binary and not which(binary):
            found.append(("yellow", who, "`%s` is not installed on THIS machine — the card may "
                                         "come from another one" % binary))
    return found

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GIT_RE = re.compile(r"^(https://|http://|git@|ssh://|file://)")
BODY_MAX = 500          # spec: "Keep your main SKILL.md under 500 lines"
DESC_MAX = 1024


# ── the registry ──────────────────────────────────────────────────────────
def read_registry(path=REGISTRY):
    """→ (header_lines, rows, problems). A row is a dict + its line number."""
    header, rows, problems = [], [], []
    if not os.path.isfile(path):
        return list(HEADER), rows, problems
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            raw = line.rstrip("\n")
            if not raw.strip() or raw.lstrip().startswith("#"):
                if not rows:
                    header.append(raw)
                continue
            cells = raw.split("\t")
            if len(cells) == len(FIELDS) - 1:
                # 🔄 a row from before the `domain` column (2026-10-03): no domain declared.
                cells.append("-")
            elif len(cells) == len(FIELDS) - 2:
                # 🔄 a row from before the `credential` column (2026-09-27): read it, and let
                # the credential rule say what it lacks — never "malformed", which hides why.
                cells.insert(FIELDS.index("credential"), "")
                cells.append("-")
            if len(cells) != len(FIELDS):
                problems.append((n, "%d field(s), the format has %d" %
                                 (len(cells), len(FIELDS))))
                continue
            row = dict(zip(FIELDS, cells))
            row["_line"] = n
            rows.append(row)
    return header, rows, problems


def write_registry(header, rows, path=REGISTRY):
    with open(path, "w", encoding="utf-8") as fh:
        for h in header:
            fh.write(h + "\n")
        for r in rows:
            fh.write("\t".join(r[f] for f in FIELDS) + "\n")


def valid_name(name):
    return 0 < len(name) <= 64 and bool(NAME_RE.match(name))


def is_authored(row):
    return row["source"].startswith("authored:")


# ⭐ An MCP server is not always a git repo (2026-10-03): `npm:<package>` pinned to an EXACT
# version (npm versions are immutable — the same guarantee a sha gives), or `remote:<https url>`,
# which has no code on this machine at all. ⛔ Never `@latest`: what runs must be what was reviewed.
NPM_VER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
MCP_JSON = os.path.join(REPO, ".mcp.json")


def is_npm(row):
    return row["source"].startswith("npm:")


def is_remote(row):
    return row["source"].startswith("remote:")


def has_code(row):
    """False for a row whose code never lives in connection/ (npm runs from npx's cache)."""
    return not (is_npm(row) or is_remote(row))


def mcp_entry(row):
    """The `.mcp.json` declaration a reviewed MCP row produces."""
    if is_npm(row):
        return {"type": "stdio", "command": "npx",
                "args": ["-y", "%s@%s" % (row["source"][4:], row["ref"])]}
    return {"type": "http", "url": row["source"][7:]}


def mcp_drift(row, declared):
    """'' when `.mcp.json` runs what the row pins, else why not. Extra args are the server's
    OPTIONS (`--headless`…) and live only in the declaration; the package@version, the command
    and the url are what was reviewed, and those must match exactly."""
    want = mcp_entry(row)
    if not isinstance(declared, dict):
        return "not an object"
    if is_npm(row):
        args = declared.get("args") or []
        if declared.get("command") != "npx" or want["args"][1] not in args:
            return "runs %s %s — the row pins %s" % (declared.get("command"),
                                                     " ".join(map(str, args))[:60], want["args"][1])
        return ""
    if declared.get("url") != want["url"]:
        return "url %s — the row pins %s" % (declared.get("url"), want["url"])
    return ""


def read_mcp_json():
    import json
    try:
        with open(MCP_JSON, encoding="utf-8") as fh:
            d = json.load(fh)
        return d if isinstance(d, dict) else {}
    except OSError:
        return {}


def write_mcp_json(d):
    import json
    with open(MCP_JSON, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def is_inner(row):
    """A skill shipped INSIDE a repo that lives in tools/ — `in:tools/<repo>/…`."""
    return row["source"].startswith("in:")


def content_dir(row):
    """Where the row's files live on disk."""
    if is_inner(row):
        return os.path.join(CONN, row["source"][3:])
    return os.path.join(CONN, TYPES.get(row["type"], "?"), row["name"])


def exposes(row):
    v = row["exposes"].strip()
    return [] if v in ("", "-") else [e.strip() for e in v.split(",") if e.strip()]


# ── the Agent Skills standard ─────────────────────────────────────────────
def _frontmatter(text):
    """→ (fields, error). Reads `key: value`, quoted values and `>`/`|` blocks."""
    if text.startswith("﻿"):
        return None, "starts with a BOM — the opening `---` must be byte 1"
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return None, "line 1 is not `---` — without it the file is not a skill"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].rstrip() == "---")
    except StopIteration:
        return None, "the frontmatter never closes with `---`"
    fields, key, block = {}, None, None
    for ln in lines[1:end]:
        if block is not None and (ln.startswith(" ") or not ln.strip()):
            fields[key] = (fields[key] + (" " if block == ">" else "\n") +
                           ln.strip()).strip()
            continue
        block = None
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", ln)
        if not m:
            continue                  # nested maps (metadata:) — values not needed
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-"):
            fields[key], block = "", val[0]
        elif len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            fields[key] = val[1:-1]
        else:
            fields[key] = val
    return {"_body_lines": len(lines) - end - 1, **fields}, None


def check_skill(folder, expect=None):
    """→ list of (level, message). level: 'red' | 'yellow'.

    `expect` = the name the agent will see it under (the LINK's name, = the row's name). A skill
    shipped INSIDE a repo keeps its upstream folder, and that folder may not match its `name`
    (taste-skill: `brutalist-skill/` declares `industrial-brutalist-ui`) — the link carries the
    declared name, exactly as `npx skills add` does, and the upstream tree is never edited."""
    out = []
    md = os.path.join(folder, "SKILL.md")
    if not os.path.isfile(md):
        return [("red", "no SKILL.md")]
    with open(md, encoding="utf-8", errors="replace") as fh:
        fm, err = _frontmatter(fh.read())
    if err:
        return [("red", "SKILL.md: " + err)]
    name, desc = fm.get("name", ""), fm.get("description", "")
    base = expect or os.path.basename(os.path.normpath(folder))
    if not name:
        out.append(("red", "`name` missing"))
    elif not valid_name(name):
        out.append(("red", "`name: %s` breaks the spec (a-z 0-9 -, ≤64, no "
                           "edge/double hyphen)" % name))
    elif name != base:
        out.append(("red", "`name: %s` ≠ folder `%s` — it will not load" %
                    (name, base)))
    if not desc:
        out.append(("red", "`description` missing — the agent cannot know "
                           "when to use it"))
    elif len(desc) > DESC_MAX:
        out.append(("red", "`description` is %d chars, the limit is %d" %
                    (len(desc), DESC_MAX)))
    if fm["_body_lines"] > BODY_MAX:
        out.append(("yellow", "body is %d lines, the spec asks under %d" %
                    (fm["_body_lines"], BODY_MAX)))
    return out


def skill_name_of(folder):
    """The `name` a SKILL.md declares, or None."""
    try:
        with open(os.path.join(folder, "SKILL.md"), encoding="utf-8") as fh:
            fm, err = _frontmatter(fh.read())
        return None if err else fm.get("name") or None
    except OSError:
        return None


# ── git ───────────────────────────────────────────────────────────────────
def git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                          text=True, timeout=300)


def head_of(folder):
    r = git(["rev-parse", "HEAD"], folder)
    return r.stdout.strip() if r.returncode == 0 else None


def is_tracked(path):
    """True when git versions this path. None when there is no repo.
    ⚠️ Not "is it ignored": in this repo an ignore rule marks the engine/instance
    frontier, and instance files are versioned on purpose with `git add -f`."""
    r = git(["ls-files", "--error-unmatch", path], MENTE)
    if "not a git repository" in r.stderr:
        return None
    return r.returncode == 0


LICENSES = (("GNU AFFERO", "AGPL-3.0"), ("GNU LESSER", "LGPL"),
            ("GNU GENERAL PUBLIC", "GPL"), ("APACHE LICENSE", "Apache-2.0"),
            ("MOZILLA PUBLIC", "MPL-2.0"), ("MIT LICENSE", "MIT"),
            ("PERMISSION IS HEREBY GRANTED, FREE OF CHARGE", "MIT"),
            ("BSD", "BSD"), ("UNLICENSE", "Unlicense"))


def read_license(folder):
    """SPDX-ish id read from the component's own LICENSE, or 'unknown'."""
    for f in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "LICENCE"):
        p = os.path.join(folder, f)
        if os.path.isfile(p):
            with open(p, encoding="utf-8", errors="replace") as fh:
                head = fh.read(4000).upper()
            for needle, spdx in LICENSES:
                if needle in head:
                    return spdx
            return "unknown"
    return "unknown"


# ── skills ON DEMAND · a skill is exposed only while the block in focus declares it ──
# ⭐ The owner, 2026-10-03: *"cuando una skill o tool debe de estar invocada, se menciona dentro de un
# bloque o una campaña … así controlamos el uso que se le está dando"*. Every linked skill puts its
# description in the context of EVERY turn, and a broad one (impeccable: "any frontend interface")
# invites the agent to use it on work that is not design. CLI, bridges, MCP and server are the
# declared exception: they are reached in very specific cases and stay as they are.
#
# A block declares in its §C:  `- SKILLS: \`impeccable\`, \`pdf-tools\``
# A campaign declares in its header:  `skills: \`x\``  — and every block it lists inherits it.
# The FOCUS is the block being worked on NOW: the last one the owner asked for, until they change topic.
FOCUS = os.path.join(MENTE, "cache", "focus.json")
BLOCK_STATES = ("active", "blocked", "archive")
_SKILLS_LINE = re.compile(r"^\s*(?:-\s*)?(?:SKILLS|skills):\s*(.*)$", re.M)
# ⭐ What a domain means in files: the suggestion fires when one of these is edited inside a
# block that has no skill of that domain attached. A domain not listed here never suggests.
DOMAIN_FILES = {
    "design": (".tsx", ".jsx", ".css", ".scss", ".sass", ".less", ".html", ".vue",
               ".svelte", ".astro"),
}


def declared_names(line_value):
    """`\\`a\\`, \\`b\\`` / `a, b` → ['a', 'b'] — the prose after a ` — ` is ignored."""
    v = line_value.split(" — ")[0]
    names = re.findall(r"`([a-z0-9-]+)`", v)
    if not names:
        names = [x.strip() for x in re.split(r"[,·]", v) if x.strip()]
    return [n for n in names if valid_name(n)]


def block_file(block):
    """work/blocks/<state>/<block>/BLOCK.md — the first state that has it, or None."""
    for st in BLOCK_STATES:
        p = os.path.join(MENTE, "work", "blocks", st, block, "BLOCK.md")
        if os.path.isfile(p):
            return p
    return None


def _read(path):
    """The text of a BLOCK.md / CAMPAIGN.md — or None, SAID OUT LOUD (CHK-CAU-003): an unreadable
    file is not a file that declares no skills, and reading it as one would hide its skills."""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as e:
        print("⬜ connection: %s unreadable (%s) · its skills NOT read" %
              (os.path.relpath(path, MENTE), type(e).__name__), file=sys.stderr)
        return None


def _skills_in(path, connections_only=False):
    text = _read(path)
    if text is None:
        return []
    if connections_only:
        m = re.search(r"^## Connections\s*\n(.*?)(?=^## |^<!-- ══|\Z)", text, re.M | re.S)
        text = m.group(1) if m else ""
    out = []
    for m in _SKILLS_LINE.finditer(text):
        out += [n for n in declared_names(m.group(1)) if n not in out]
    return out


def campaign_of_block(block):
    """(campaign id, CAMPAIGN.md path) of the campaign whose `## Blocks` lists it, or (None, None)."""
    import glob
    for cpath in sorted(glob.glob(os.path.join(MENTE, "work", "campaigns", "*", "CAMPAIGN.md"))):
        txt = _read(cpath)
        if txt is None:
            continue
        m = re.search(r"^##\s*Blocks\s*\n(.*?)(?=^## |\Z)", txt, re.M | re.S)
        if m and re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(block), m.group(1)):
            return os.path.basename(os.path.dirname(cpath)), cpath
    return None, None


def block_skills(block):
    """→ (own, inherited, campaign): the skills a block declares and the ones its campaign adds."""
    bf = block_file(block)
    own = _skills_in(bf, connections_only=True) if bf else []
    cid, cpath = campaign_of_block(block)
    inherited = []
    if cpath:
        head = (_read(cpath) or "").split("\n## ", 1)[0]
        for m in _SKILLS_LINE.finditer(head):
            inherited += [n for n in declared_names(m.group(1)) if n not in inherited]
    return own, inherited, cid


def read_focus():
    """→ dict: {block, since, by, suggested: [...]} or {} when nothing is in focus."""
    import json
    try:
        with open(FOCUS, encoding="utf-8") as fh:
            d = json.load(fh)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def write_focus(d):
    import json
    os.makedirs(os.path.dirname(FOCUS), exist_ok=True)
    tmp = FOCUS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, FOCUS)


def focus_set():
    """The on-demand skills the current focus switches on → (block or None, set of names)."""
    b = read_focus().get("block")
    if not b:
        return None, set()
    own, inh, _cid = block_skills(b)
    return b, set(own) | set(inh)


def all_declarations():
    """[(who, path, [names])] — every block (any state) and every campaign that declares skills."""
    import glob
    out = []
    for st in BLOCK_STATES:
        for bf in sorted(glob.glob(os.path.join(MENTE, "work", "blocks", st, "*", "BLOCK.md"))):
            names = _skills_in(bf, connections_only=True)
            if names:
                out.append(("block %s" % os.path.basename(os.path.dirname(bf)), bf, names))
    for cpath in sorted(glob.glob(os.path.join(MENTE, "work", "campaigns", "*", "CAMPAIGN.md"))):
        head = (_read(cpath) or "").split("\n## ", 1)[0]
        names = []
        for m in _SKILLS_LINE.finditer(head):
            names += declared_names(m.group(1))
        if names:
            out.append(("campaign %s" % os.path.basename(os.path.dirname(cpath)), cpath, names))
    return out
