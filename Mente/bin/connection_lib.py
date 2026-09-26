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
