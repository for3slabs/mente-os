#!/usr/bin/env python3
"""probe-third-party — is third-party code skipped by every walker, and ONLY it?

🔴 WHY IT EXISTS (EXT-52, 2026-10-03). A repo fetched into `connection/tools/` is somebody
else's code: `registry.tsv` governs it and `check-connection` verifies it. Measured on the
engine before the fix: a planted tool put 8 red findings in `check-document`, and the
battery template copied the whole tree — tools included — into every probe.

⭐ The fix is ONE reader, `connection_lib.third_party`, used by `check-document` (both of
its walks) and by `connection_lib.tree_ignore` (the battery template). So this probe
measures both halves, because each alone would pass a broken fix:
  · third-party content is SKIPPED (①③)
  · ⛔ and the skip is NOT GLOBAL: the same defect in our own files is still caught
    (②④) — a validator that skipped everything would pass the first half perfectly.

Runs in a throwaway copy of the tree; every subject is planted there.
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
sys.path.insert(0, os.path.join(ROOT, "bin"))
import connection_lib                                # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-thirdparty-")
T = os.path.join(WORK, "Mente")


def case(label, ok, detail=""):
    print("  %-66s %s %s" % (label, "✅" if ok else "\U0001f534", detail))
    results.append((label, ok))


def put(rel, data, mode="w"):
    p = os.path.join(T, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        fh.write(data)
    return p


def doc():
    r = subprocess.run([sys.executable, os.path.join(T, "bin", "check-document")],
                       cwd=T, capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


try:
    shutil.copytree(ROOT, T, ignore=shutil.ignore_patterns(
        "__pycache__", ".beats", ".test-lock", ".git", "cache", "tools"))
    os.makedirs(os.path.join(T, "connection", "tools"), exist_ok=True)
    shutil.copy2(os.path.join(ROOT, "connection", "tools", "README.md"),
                 os.path.join(T, "connection", "tools", "README.md"))
    rc0, out0 = doc()

    # a third-party repo with every defect the document contract would catch
    TOOL = "connection/tools/zzprobe-tool"
    put(TOOL + "/README.md", "# A tool\n\nSee [the guide](docs/missing.md).\n")
    put(TOOL + "/Bad_Name_Doc.md", "no header at all\n")
    put(TOOL + "/tests/fixtures/broken.md", b"# bad \xff\xfe\xc3\x28 bytes\n", "wb")
    rc, out = doc()
    case("① a tool's headerless, broken-unicode docs → check-document never names them",
         rc == rc0 and "zzprobe-tool" not in out, "rc %d (baseline %d)" % (rc, rc0))

    # ② ⛔ not global: connection/tools/README.md is OURS
    readme = os.path.join(T, "connection", "tools", "README.md")
    keep = open(readme, encoding="utf-8").read()
    put("connection/tools/README.md", "no header at all\n")
    rc, out = doc()
    case("② ⛔ …but connection/tools/README.md is ours → its defect is still 🔴",
         rc == 1 and "connection/tools/README.md" in out, "rc %d" % rc)
    put("connection/tools/README.md", keep)

    # ③ the battery template leaves the repo out and keeps our README
    dst = os.path.join(WORK, "copy")
    shutil.copytree(T, dst, ignore=connection_lib.tree_ignore(T, ".git", "__pycache__"))
    case("③ tree_ignore → the battery copy has no third-party repo, keeps tools/README.md",
         not os.path.exists(os.path.join(dst, "connection", "tools", "zzprobe-tool"))
         and os.path.isfile(os.path.join(dst, "connection", "tools", "README.md")), "")

    # ④ ⛔ not global: the same headerless doc OUTSIDE tools/ is still caught
    put("docs/zzprobe-ours.md", "no header at all\n")
    rc, out = doc()
    case("④ ⛔ the same defect in a doc of ours → still 🔴",
         rc == 1 and "docs/zzprobe-ours.md" in out, "rc %d" % rc)
finally:
    plat.rmtree(WORK)

sys.exit(report(results))
