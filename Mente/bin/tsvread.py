"""tsvread — ONE reader for the tab-separated tables this engine keeps.

🔴 THE FAILURE THAT MADE THIS NECESSARY. `CHK-SHR-001` says a shape read in
several places gets ONE reader, and its own note records four copies of a block
reader that had already diverged. ⛔ Measured 2026-09-02: **six copies** of the
same eight lines — `bin/init`, `bin/check-accounts`, `bin/connect-account`,
`bin/check-structure`, `bin/check-declared`, `hooks/gate-accounts.py`.

⚠️ And they had already drifted apart from the truth: `pieces.tsv` declares its
columns on a line that does not start with `#`, so every copy read the HEADER as
a row — 177 where 176 exist, one of them a piece named `piece` at a path named
`path`. ⭐ Fixing that in six places is how the seventh copy gets it wrong.

⭐ What this skips, and why each:
  · `#` comments — the tables are documented in place
  · blank lines
  · ⭐ THE HEADER ROW, by its first cell, whether or not it carries a `#`

⚠️ It never raises. A table that cannot be read yields an empty list and the
caller says so — ⛔ a parser that throws turns one unreadable file into a crash,
and a crash reports nothing at all (`CHK-CAU-002`).

🔴 **But EMPTY and ABSENT are different answers**, and collapsing them was a
defect this refactor introduced: `bin/connect-account` returned `None` for "no
registry" by catching the `OSError`, and once the reader swallowed it, a missing
registry read as an empty one. ⭐ `exists()` is what tells them apart.
"""

# ⭐ The first cell of a header, per table. Read as data, each becomes a piece
# or an account that does not exist.
# ⚠️ MEASURED, not guessed: the six copies patched the header FOUR different
# ways — `f[0] == "piece"`, `== "repo"`, `in ("repo", "")`, and one with `!=`.
# ⛔ That spread is the divergence CHK-SHR-001 warns about, already happened.
HEADERS = ("piece", "repo", "account", "name", "id", "#")


def exists(path):
    """⭐ Is the table THERE? ⛔ An empty table and an absent one are different
    answers, and only the caller knows which of the two is a defect."""
    import os
    return os.path.exists(path)


def rows(path, want=0):
    """(line number, [cells]) for every DATA row of a TSV table.

    ⭐ The line number is always returned; a caller that does not need it
    ignores it. ⛔ Two variants — one with the count, one without — is how six
    copies became six chances to diverge.

    `want` drops rows with fewer than that many cells: a truncated line is not
    a row, and reporting it as one blames the table for a defect in itself.
    """
    out = []
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        # ⬜ NOT MEASURED, never an empty table: the caller is the one that
        # knows whether an absent table is a gap or a normal state.
        return out
    with fh:
        for n, line in enumerate(fh, 1):
            if line.startswith("#") or not line.strip():
                continue
            cells = [c.strip() for c in line.rstrip("\n").split("\t")]
            if not cells or not cells[0]:
                continue          # ⬜ a row with no first cell names nothing
            if cells[0].strip("# ").lower() in HEADERS:
                continue          # ⭐ the header, marked or not
            if want and len(cells) < want:
                continue
            out.append((n, cells))
    return out
