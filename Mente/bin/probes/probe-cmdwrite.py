#!/usr/bin/env python3
"""probe-cmdwrite — proves the engine can see a write that arrives through Bash.

🔴 THE FAILURE THAT MADE THIS FILE, measured 2026-09-07 on a real Windows run.
A whole project was built and shipped — nine files — and NOT ONE gate fired.
The gates were wired, alive, and leaving beats when called by hand. ⛔ The
assistant simply never used the door they watch: it wrote every file with
`cat > path <<'EOF'` from Bash, and the write gates were on
`Edit|Write|MultiEdit`. Measured in the transcript: **Bash 83 uses ·
Write/Edit 0.**

⭐ THE LESSON, and it is the engine's own thesis turned one notch: a gate that
watches a door nobody walks through reports green forever. ⛔ Wiring is not
coverage — the question is not "is the gate installed" but "does every way of
writing reach it".

⚠️ AND THE OTHER HALF, which decides whether the system survives: it must NOT
refuse `npm install`, `git commit` or a read. 🔴 A gate that refuses ordinary
tooling is switched off within a day (ADR-012), and then nothing is governed.
"""
import os, sys
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
from cmdwrite import writes                          # noqa: E402

results = []


def case(label, ok, detail=""):
    print("  %-56s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def eq(label, cmd, expected):
    got = writes(cmd)
    case(label, got == expected, "" if got == expected
         else "got %r, expected %r" % (got, expected))


print("═══ PROBE · cmdwrite ═══\n")

# ── ⭐ THE MEASURED FAILURE ITSELF ─────────────────────────────────────────
eq("① 🔴 ⭐ `cat > path <<EOF` — the exact form that shipped unseen",
   "cat > site/x.md <<'EOF'\nhola\nEOF", ["site/x.md"])
eq("② `cat >>` appends, and that is still a write", "cat >> a.md", ["a.md"])
eq("③ `echo >` writes", "echo hi > nota.txt", ["nota.txt"])
eq("④ `printf >` writes", "printf x > b.txt", ["b.txt"])
eq("⑤ `tee` writes its argument", "cat a | tee out.log", ["out.log"])
eq("⑥ `sed -i` edits in place", "sed -i s/a/b/ f.md g.md", ["f.md", "g.md"])
eq("⑦ `cp` writes its destination, not its source", "cp a b", ["b"])
eq("⑧ an interpreter naming a write is a write",
   'python3 -c "open(\'z.md\',\'w\')"', ["z.md"])

# ── ⛔ AND WHAT IT MUST NOT CALL A WRITE ───────────────────────────────────
# 🔴 The direction that gets a gate REMOVED. A refusal here costs the whole
# system, so each of these is as load-bearing as the cases above.
eq("⑨ ⛔ `npm install` writes nothing the person governs", "npm install", [])
eq("⑩ ⛔ `git commit` neither", "git commit -m x", [])
eq("⑪ ⛔ reading is not writing", "ls -la && grep x f", [])
eq("⑫ ⛔ `2> /dev/null` is not a file somebody authored",
   "cat a 2> /dev/null", [])
eq("⑬ ⛔ `2>&1` is a descriptor, not a path", "cat a > out.txt 2>&1",
   ["out.txt"])

# ── ㉙ 🔴 A `>` INSIDE QUOTES IS DATA, NOT A REDIRECTION ───────────────────
# 🔴 THE FAILURE, measured 2026-09-08 on a real install. `grep -rn "a > b" x/`
# was REFUSED twice during an audit: the `>` lives inside a quoted search
# pattern and the matcher read it as "writes to the file b". ⛔ A read-only
# grep rejected as a write is what makes somebody switch the gate off — and its
# way out disables the gate entirely (ADR-012).
eq("㉙ 🔴 ⭐ a `>` inside double quotes writes nothing",
   'grep -rn "len(p) > 4" Mente/', [])
eq("㉙b ⭐ and inside single quotes either", "grep 'a > b' x/", [])
eq("㉙c ⛔ but a real write in the SAME line is still seen",
   'grep "a > b" x/ && echo y > out.txt', ["out.txt"])

# ⛔ AND THE ONE PLACE A QUOTED STRING IS NOT DATA: the destination itself.
# 🔴 Caught while writing the fix above — masking every quoted string also hid
# `cat > "my dir/a b.md"`, so a legitimate write to a path WITH A SPACE came
# back as `xxxxxxx`. A fix that breaks the case beside it is not a fix.
eq("㉙d ⛔ a QUOTED redirection target survives the masking",
   'cat > "mi dir/a b.md"', ["mi dir/a b.md"])
eq("㉙e ⛔ and an appended one too",
   'echo x >> "log dir/a.txt"', ["log dir/a.txt"])

# ── ⬜ AND WHAT IT MUST REFUSE TO GUESS ────────────────────────────────────
# ⚠️ Three answers, not two. ⛔ `None` collapsed into `[]` is a hole; collapsed
# into "everything" it refuses correct work. The caller must tell them apart.
eq("⑭ ⬜ an unknown verb is NOT MEASURED, never assumed safe",
   "herramienta-rara x", None)
eq("⑮ ⬜ unbalanced quoting is NOT MEASURED, never a partial path",
   'cat > "sin cerrar', None)
eq("⑯ ⬜ a destination the engine cannot name is NOT MEASURED",
   'cat > "$DEST"', None)

# ── ⛔ THE BOUNDARIES THAT BROKE WHEN FIRST WRITTEN ────────────────────────
# Each of these returned a WRONG path before it was fixed, and a wrong path is
# worse than no path: the gate then judges a file nobody is writing and waves
# through the one that is.
# 🔴 Caught while sabotage-testing THIS case: the first version used a body
# saying `rm -rf`, which contains no redirection — so deleting the heredoc
# stripper changed nothing and the case passed against broken code. ⛔ The body
# must contain the very thing the reader looks for, or it measures a
# coincidence. This one documents a redirection, as a README would.
eq("⑰ ⛔ a heredoc BODY is data — a redirection inside it is not a command",
   "cat > doc.md <<'EOF'\nRun: echo hi > /etc/passwd\nEOF", ["doc.md"])
eq("⑱ ⛔ a quoted path keeps its spaces", 'cat > "mi carpeta/a b.md"',
   ["mi carpeta/a b.md"])
eq("⑲ ⛔ subshell parentheses are grouping, not path text",
   "(cd x && cat > y.md)", ["y.md"])
eq("⑳ ⛔ `sudo` is a prefix, not the verb", "sudo tee /etc/hosts",
   ["/etc/hosts"])
eq("㉑ ⛔ a VAR=value prefix is not the verb", "FOO=bar cat > z.md", ["z.md"])
eq("㉒ ⭐ every write in a chain, not just the first",
   "echo a > x.md && echo b > y.md", ["x.md", "y.md"])
eq("㉓ ⛔ a Windows path survives whole", r"cat > C:\dev\x.md",
   [r"C:\dev\x.md"])

# ── ⛔ IT NEVER CRASHES ────────────────────────────────────────────────────
# ⚠️ A hook that raises prints a trace and lets the action through: it does not
# protect, it only looks like it.
for label, bad in (("㉔ empty", ""), ("㉕ None", None), ("㉖ a number", 7),
                   ("㉗ a list", []), ("㉘ heredoc never closed",
                                       "cat > a.md <<EOF\nsin fin")):
    try:
        writes(bad)
        case("%s · does not crash" % label, True)
    except Exception as e:                                    # noqa: BLE001
        case("%s · does not crash" % label, False, type(e).__name__)

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
# ⭐ Declared, not implied. This probe reads strings and touches no disk, and
# the battery requires every probe to SAY so — an absent declaration and a
# probe that quietly littered look identical from outside.
print("  leftovers: none")
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
sys.exit(0 if good == len(results) else 1)
