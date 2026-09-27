"""connection_lib — the ONE implementation of what connection/ means.

⭐ Read by `bin/connection` (the installer) and `bin/check-connection` (the
verifier). Two scripts that each carried their own copy of "what a valid skill
is" would drift, and the verifier would bless what the installer never wrote.

What lives here: the registry format · where a row's content lives · the Agent
Skills rules (agentskills.io/specification, read 2026-09-26) · the link paths.
⛔ No third-party YAML parser: the engine runs on a bare Python, so the
frontmatter reader below handles the subset a SKILL.md uses and says so when
it meets something it cannot read.
"""
import os
import re
import subprocess

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
    "# Format (TAB-separated): name  type  source  ref  state  installed  license  exposes  why",
    "#   name      = folder name under <type>/ · [a-z0-9-], 1-64, no leading/trailing/double hyphen",
    "#   type      = skill | mcp | tool",
    "#   source    = git URL · \"authored:<path>\" when WE wrote it (a SKILL.md for a repo that had none)",
    "#   ref       = the full commit sha it is pinned to · \"-\" only for authored",
    "#   state     = quarantine (fetched, not reviewed, NOT exposed) · active · disabled",
    "#   installed = YYYY-MM-DD",
    "#   license   = SPDX id read from the component's LICENSE · \"unknown\" is a finding, not a value",
    "#   exposes   = where the agent sees it, comma-separated, from the project root:",
    "#               .claude/skills/<name> · .agents/skills/<name> · .mcp.json:<name> · \"-\"",
    "#   why       = who asked and for what, one line",
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


def check_skill(folder):
    """→ list of (level, message). level: 'red' | 'yellow'."""
    out = []
    md = os.path.join(folder, "SKILL.md")
    if not os.path.isfile(md):
        return [("red", "no SKILL.md")]
    with open(md, encoding="utf-8", errors="replace") as fh:
        fm, err = _frontmatter(fh.read())
    if err:
        return [("red", "SKILL.md: " + err)]
    name, desc = fm.get("name", ""), fm.get("description", "")
    base = os.path.basename(os.path.normpath(folder))
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
