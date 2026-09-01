#!/usr/bin/env python3
"""The sabotage harness — one place, so every probe verifies the same way.

⭐ A probe answers ONE question: does this check detect what it claims?
⛔ And "it failed" does not answer it. A red for the wrong reason, or a
   validator that died, prove nothing (rules/rule-checks-must-measure.md §3).

VERDICTS
  PASS          the valid state was accepted
  FAIL          ⭐ the broken state was detected, and the message names the cause
  WRONG_CAUSE   ⚠️ it failed — for something else
  CRASH         🔴 no verdict at all
  NOT_DETECTED  🔴 it stayed green on a broken state
  SKIP          it does not apply here, and it says so

⚠️ A probe has its own failure modes (§7 of that rule). This harness closes
   all three: it cleans everything it creates, it hands fixtures their real
   identity, and its filter is derived from what it plants — never narrower.
"""
import os, re, shutil, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ⭐ The marker must not itself violate a rule the system checks: an underscore
# made every fixture trip DOC-NAM-001, and the probe read its own naming as
# the checker misbehaving. A probe that breaks a rule cannot measure it.
MARK = "zzprobe"         # every fixture carries it, so the filter cannot be narrower


class Probe:
    def __init__(self, checker, id_prefix, also=()):
        self.checker = checker
        self.rx = re.compile(r"%s-[A-Z]+-\d+" % id_prefix)
        self.made = []       # ⭐ everything created, so cleanup cannot miss one
        self.results = []
        # ⭐ Probe failure mode #3: a filter narrower than what the probe
        # touches. Some cases EDIT an existing file instead of planting a
        # fixture, and its findings carry no marker — filtering on the marker
        # alone reports a working check as undetected.
        self.also = tuple(also)

    def _mine(self, out):
        keys = (MARK,) + self.also
        return [l for l in out.splitlines() if any(k in l for k in keys)]

    # ── lifecycle ────────────────────────────────────────────────────────
    def track(self, path):
        self.made.append(path)
        return path

    def clean(self):
        for p in self.made:
            shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (
                os.path.exists(p) and os.remove(p))
        self.made = []

    def run(self):
        """Run the checker as a SCRIPT — the way it actually runs.
        ⛔ An exec() never sets __name__ == '__main__', so a crash guard would
        not execute and a protected validator would read as unprotected."""
        r = subprocess.run([sys.executable, "bin/" + self.checker, "--quiet"],
                           cwd=ROOT, capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr

    # ── the verdict ──────────────────────────────────────────────────────
    def verdict(self, want_id):
        code, out, err = self.run()
        mine = self._mine(out)
        ids = sorted({m for l in mine for m in self.rx.findall(l)})

        if "Traceback" in err or "Traceback" in out:
            return "CRASH", ids, err.strip().splitlines()[-1:] or [""]
        if "crashed ·" in out:
            return "CRASH", ids, [l for l in out.splitlines() if "crashed" in l]
        if not ids:
            return "NOT_DETECTED", ids, mine
        if want_id in ids:
            return "FAIL", ids, mine
        return "WRONG_CAUSE", ids, mine

    def case(self, label, setup, want_id):
        self.clean()
        setup()
        v, ids, detail = self.verdict(want_id)
        mark = {"FAIL": "✅", "WRONG_CAUSE": "⚠️", "CRASH": "🔴",
                "NOT_DETECTED": "🔴"}[v]
        shown = v if v == "FAIL" else "%s → %s" % (v, " ".join(ids) or "—")
        print("  %-46s %s %-22s %s" % (label, mark, shown, " ".join(ids)))
        if v == "CRASH" and detail:
            print("       %s" % detail[0][:100])
        self.clean()
        self.results.append((label, v))
        return v == "FAIL"

    def inverse(self, label, setup):
        """⭐ The reverse test: a CORRECT state must not fire.
        A check only ever proven on broken input has not been shown to
        discriminate — and an alarm that fires too often is switched off just
        as fast as one that never fires."""
        self.clean()
        setup()
        code, out, err = self.run()
        mine = self._mine(out)
        ok = not mine
        print("  %-46s %s %s" % (label, "✅" if ok else "🔴",
                                 "does NOT fire (correct)" if ok
                                 else "false positive: " + mine[0][:70]))
        self.clean()
        self.results.append((label, "PASS" if ok else "FALSE_POSITIVE"))
        return ok

    def baseline(self):
        self.clean()
        code, out, err = self.run()
        noise = [l for l in out.splitlines() if "🔴" in l]
        print("  %-46s %s\n" % ("⓪ the real tree, untouched",
                                "✅ 0 hallazgos" if not noise
                                else "🔴 %d preexistentes:\n     %s"
                                % (len(noise), "\n     ".join(noise[:3]))))
        return not noise

    def crash_guard(self):
        """CHK-CAU-002 · an exception must come out as a finding, not a trace."""
        src = open(os.path.join(ROOT, "bin", self.checker), encoding="utf-8").read()
        p = self.track(os.path.join(ROOT, "bin", "%s-crash%s" % (MARK, "")))
        open(p, "w", encoding="utf-8").write(
            src.replace("def main():", 'def main():\n    raise RuntimeError("boom")', 1))
        r = subprocess.run([sys.executable, p], cwd=ROOT, capture_output=True, text=True)
        ok = "crashed ·" in r.stdout and "Traceback" not in r.stdout
        print("  %-46s %s %s" % ("⑨ CRASH · reported as a finding",
                                 "✅" if ok else "🔴",
                                 "reportado, no un trace" if ok
                                 else (r.stdout or r.stderr).strip()[:70]))
        self.clean()
        self.results.append(("crash guard", "PASS" if ok else "FAIL"))
        return ok

    def report(self):
        self.clean()
        good = sum(1 for _, v in self.results if v in ("FAIL", "PASS"))
        bad = [(l, v) for l, v in self.results if v not in ("FAIL", "PASS")]
        print("\n  ➜ %d of %d correct" % (good, len(self.results)))
        for l, v in bad:
            print("     🔴 %-42s %s" % (l, v))
        leftovers = [p for p in glob.glob(os.path.join(ROOT, "**", MARK + "*"),
                                          recursive=True)]
        print("\n  leftovers: %s" % (leftovers or "none"))
        r = subprocess.run([sys.executable, "bin/" + self.checker], cwd=ROOT,
                           capture_output=True, text=True)
        print("  state: %s" % r.stdout.strip().replace("\n", "\n          "))
        return not bad and not leftovers
