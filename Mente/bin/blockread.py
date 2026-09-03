"""blockread — ONE reader for a block's sections. Shared on purpose.

⛔ This existed as four copies, one per validator, and the three comparable
ones had already diverged. Two of them could not see a section headed by its
NAME, so every section came back empty and the checks that read them reported
findings against a file they had not read.

> ⭐ ONE SHAPE, ONE READER. Two readers over one shape diverge; one cannot.

⬜ What a section is CALLED belongs to the installation. The engine fixes only
WHAT must be answered — so all three real shapes are accepted:

    ## K · Closing          the letter, with a separator
    <!-- ══ K · … ══ -->    an HTML marker, with the visible heading after it
    ## Closing              the name alone, no letter

⛔ NOT for every markdown document. This reader knows the vocabulary of a
BLOCK. A decision record is headed `Context` / `Decision` / `Rationale` and has
no letters at all — pointing this reader at one returns nothing, and "nothing"
reads exactly like "the section is empty". ⭐ The criterion is
`CHK-SHR-001/002` in rules/rule-checks-must-measure.md — ⛔ stated there rather
than restated here, because a criterion repeated is a criterion that diverges.
"""
import re
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

NAMES = {"A": "identity", "B": "scope", "C": "connections",
         "D": "required standards", "E": "state", "F": "sub-?blocks",
         "G": "decisions", "H": "friction", "I": "checkpoints",
         "J": "context", "K": "closing"}

SEC = re.compile(r"^(?:##[ \t]*([A-K])[ \t]*[·.:-]"
                 r"|<!--[^\n]*?\b([A-K])[ \t]*[·.:-][^\n]*?-->)", re.M)


def sections(text):
    """Every section letter present, in any of the three shapes."""
    found = {(m.group(1) or m.group(2)) for m in SEC.finditer(text)}
    for letter, name in NAMES.items():
        if letter in found:
            continue
        if re.search(r"^##\s*%s\b" % name, text, re.M | re.I):
            found.add(letter)
    return found


def order(text):
    return [(m.group(1) or m.group(2)) for m in SEC.finditer(text)]


def body_of(text, letter):
    """Everything between this section's marker and the next one."""
    m = re.search(r"^(?:##\s*%s\s*[·.:-]|<!--[^\n]*?\b%s\s*[·.:-][^\n]*?-->"
                  r"|##\s*%s\b).*?$"
                  % (letter, letter, NAMES.get(letter, letter)),
                  text, re.M | re.I)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = SEC.search(rest)
    # ⭐ When the section was found by an HTML marker, the MARKERS are the
    # boundaries: every `## …` until the next marker is a subsection of this
    # one. A real §Scope holds `## ✅ IN` and `## ⛔ OUT` and no heading of its
    # own — cutting at the first `##` returned an empty scope for every block.
    alt = None
    if not m.group(0).lstrip().startswith("<!--"):
        alt = re.search(r"^##\s+\S.*$", rest, re.M)
    ends = [x.start() for x in (nxt, alt) if x]
    return rest[:min(ends)] if ends else rest


# ⛔ Only a value shaped like a block id counts as a dependency. Measured on
# nine real blocks: `nada`, `nothing`, `the` — the word "none" in two languages
# and an article lifted out of a prose sentence — all read as missing blocks.
# ⬜ The "none" WORD is the installation's language; the SHAPE is not.
DEPENDS = re.compile(r"(?:DEPENDS ON|BLOCKED BY|FEEDS|depends on|requires)"
                     r"\s*:?\s*`?([A-Za-z0-9][\w-]*(?:[-_][\w-]+)+)`?", re.I)
NONE_WORDS = re.compile(r"(none|nothing|nada|n/?a|tbd|pending)\W?$", re.I)


def dependencies(section_body):
    """Every block id this section declares a dependency on."""
    return [d for d in DEPENDS.findall(section_body) if not NONE_WORDS.match(d)]
