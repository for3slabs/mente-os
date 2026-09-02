#!/usr/bin/env python3
"""run-all — every probe, one run. ⭐ The only thing that matters is 0 failed.

A green here means each validator has been SEEN to fail on a state that
breaks what it claims to measure, with the message naming the real cause.
⛔ A validator with no probe is unproven, and this reports that too.
"""
import os, time, re, subprocess, sys, glob, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.dirname(HERE)

# ── 🔴 THE RECURSION GUARD · this cost the machine once ─────────────────────
# 🔴 MEASURED, 2026-09-01: a generator read the battery's result by RUNNING the
# battery. The battery runs every probe; one probe exercises that generator;
# that generator ran the battery. Ten of these probes copy the whole tree into a
# temporary directory first, so each level spawned a full suite AND a full copy.
# ⛔ It reached 655 live processes, load average 609, and 2,800 abandoned copies
# before it was stopped by hand.
#
# ⚠️ IT DID NOT LOOK LIKE A LOOP. It looked like slowness — the first symptom was
# a probe timing out, which is the most ordinary failure there is.
#
# ⭐ THE FIX IS STRUCTURAL, NOT A RULE. Nobody can be trusted to remember not to
# invoke the battery from something the battery invokes: the call is three files
# away from where the loop closes. So the battery marks its own descendants, and
# refuses to be one.
if os.environ.get("MENTE_BATTERY_RUNNING") == "1":
    print("⛔ REFUSED · the battery is already running in a parent process.\n"
          "   Something the battery invoked tried to invoke it back — that is a\n"
          "   loop, and each turn of it copies the tree and spawns a full suite.\n"
          "   ⭐ Read the last result from cache/last-battery.txt instead.",
          file=sys.stderr)
    sys.exit(2)
os.environ["MENTE_BATTERY_RUNNING"] = "1"

probes = sorted(glob.glob(os.path.join(HERE, "probe-*.py")))
# ⛔ Not every validator is named `check-*`. Filtering on that prefix left
# `grade-block` out of the count, so coverage read "13 validators, 14 probes" —
# a filter narrower than what exists, which reports a covered tree as
# inconsistent and an uncovered one as complete.
VALIDATORS = ("check-", "grade-")
checkers = sorted(f for f in os.listdir(BIN)
                  if f.startswith(VALIDATORS) and os.path.isfile(os.path.join(BIN, f)))

# ⭐ WHY EACH PROBE GETS ITS OWN COPY OF THE TREE
#
# Five probes edit SHARED state — base-rules, a contract, the project rules —
# to plant their defect. Run side by side in one tree they overwrite each
# other, and the result is not slow: it is FALSE.
#
# ⛔ Measured, before choosing this: running the nine isolated ones in parallel
# and the five sharing ones in series took 14.2s against 11.1s in plain
# sequence — disk contention ate the gain. Copying the whole tree costs 0.04s
# for ~100 files, so isolation is cheaper than the contention it removes.
#
#    plain sequence  11.1s  ·  hybrid  14.2s  ·  isolated + parallel  4.5s
#
# ⚠️ THOSE NUMBERS ARE FROM 14 PROBES. Today there are 38 and the suite takes
# ~15 s — ⛔ which reads as a 3.3× degradation and is not one: per probe it went
# 0.32 s → 0.41 s, and today's probes carry more cases each (probe-document
# alone has 58). ⭐ A total compared against a total with a different
# denominator is the arithmetic that turns growth into alarm.
#
# ⬜ MENTE_PROBES_SERIAL=1 forces the old behaviour, for debugging a probe
# whose failure only appears in the real tree.
ROOT = os.path.dirname(BIN)
SERIAL = os.environ.get("MENTE_PROBES_SERIAL") == "1"
_IGNORE = shutil.ignore_patterns(".git", "__pycache__", "cache", "*.pyc")


def run_probe(q):
    """Run one probe. In isolated mode it gets a private copy of the tree, so
    what it edits cannot reach any other probe — ⛔ and cannot reach the real
    tree either, which is the second reason this is worth the copy."""
    name = os.path.basename(q)[:-3]
    if SERIAL:
        return name, subprocess.run([sys.executable, q],
                                    capture_output=True, text=True)
    d = tempfile.mkdtemp(prefix="mente-probe-")
    try:
        tree = os.path.join(d, os.path.basename(ROOT))
        shutil.copytree(ROOT, tree, ignore=_IGNORE)
        return name, subprocess.run(
            [sys.executable, os.path.join(tree, "bin", "probes", name + ".py")],
            cwd=tree, capture_output=True, text=True,
            env=dict(os.environ, MENTE_PROBE_ISOLATED="1"))
    finally:
        shutil.rmtree(d, ignore_errors=True)


print("═══ TODAS LAS SONDAS ═══%s\n"
      % ("" if not SERIAL else "  (serial · MENTE_PROBES_SERIAL=1)"))
_started = time.time()
total = failed = 0
rows = []

if SERIAL:
    results = [run_probe(q) for q in probes]
else:
    # ⭐ TWELVE, and the number matters less than the reason. Measured on a
    # 16-core WSL box with 7 GB, on an IDLE machine:
    #   12 → 14.1-17.2 s · 16 → 15.0 s · 24 → 13.7-17.2 s
    # ⛔ The three ranges OVERLAP: the spread within one setting (±3 s) is wider
    # than the gap between settings, so "24 is faster" is not a claim this box
    # supports. ⚠️ An earlier reading called 16 worse than 8 — that was taken
    # with the machine loaded by the measurement itself.
    # ⭐ What IS measured: the serial sum is 30.2 s and the slowest probe is
    # 4.3 s, so the floor is ~4 s and the rest is per-probe overhead — each one
    # gets a private COPY of the tree (isolation, 1.0 s total) and runs ~21%
    # slower from it. ⛔ Adding workers cannot close that gap.
    with ThreadPoolExecutor(max_workers=min(12, len(probes))) as _ex:
        results = list(_ex.map(run_probe, probes))

# ⭐ A CASE LABEL IS AN ADDRESS — the same rule ids obey (DOC-IDS-001).
# ⛔ Measured in probe-document: two sections each restarted their numbering, so
# five numerals addressed two cases each and a failure reported as ㉕ had two
# possible homes. ⚠️ Cheap while a probe is green; it costs exactly when the
# numeral is read, which is when something broke.
# ⭐ Checked HERE and not in the harness: 23 of the 30 probes print their own
# results and never construct a Probe, so a guard living in the harness would
# cover seven and read as if it covered all of them.
# ⚠️ NUMERALS ONLY — ⛔ not every leading marker. The first version counted any
# non-ascii token that opened a line, so a probe's ⬜ notice and its ⭐ heading
# read as colliding cases: seven of the fifteen it reported were prose, and a
# guard that cries wolf on prose is switched off.
_NUMERAL = re.compile(r"^ {2}([\u2460-\u24FF\u3251-\u32BF])(\w?)\s", re.M)


def duplicate_labels(out):
    """The numerals a probe used more than once, read from its printed lines.

    ⭐ A suffix is part of the address: ⑭ and ⑭b are two cases, not one used
    twice — inserting a lettered case is how a probe grows without renumbering.
    """
    seen = {}
    for base, suffix in _NUMERAL.findall(out):
        seen[base + suffix] = seen.get(base + suffix, 0) + 1
    return sorted(k for k, n in seen.items() if n > 1)


for name, r in results:
    # ⭐ The probe's own tally line. ⚠️ While the output was being translated
    # this accepted both spellings — ⛔ and the tolerance was REMOVED once the
    # last probe was done, because a parser that accepts a wording nothing
    # produces is a parser nobody can reason about.
    m = re.search(r"➜ (\d+) of (\d+) correct", r.stdout)
    leftovers = "leftovers: none" not in r.stdout
    if not m:
        # 🔴 A PROBE THAT NEVER REPORTED ITS TALLY DID NOT RUN — it crashed, or
        # it died before its last line. ⛔ Scored as (0, 0) this passed the
        # `good == all_` test and printed "0/0", which reads as "no cases" and
        # not as "it died"; worse, it contributed NOTHING to the total, so the
        # battery's headline number shrank silently while still saying 0 failed.
        # ⚠️ Found on a clean clone: a probe assumed an instance file existed.
        # ⭐ Counted as ONE failure so the total can never quietly shrink.
        crash = (r.stderr.strip().splitlines() or ["no output"])[-1]
        total += 1
        failed += 1
        rows.append((name, 0, 1, False, leftovers))
        print("  %-24s 🔴 CRASHED · %s" % (name, crash[:60]))
        continue
    good, all_ = int(m.group(1)), int(m.group(2))
    dups = duplicate_labels(r.stdout)
    if dups:
        # ⭐ One failure, not one per numeral: the defect is the probe's
        # numbering, and reporting it five times would rank a labelling slip
        # above a validator that stopped working.
        total += 1
        failed += 1
        print("  %-24s 🔴 case label used twice: %s"
              % (name, " ".join(dups)[:44]))
    ok = r.returncode == 0 and good == all_ and not leftovers and not dups
    total += all_
    failed += all_ - good
    rows.append((name, good, all_, ok, leftovers))
    print("  %-24s %s %s/%s%s" % (name, "✅" if ok else "🔴", good, all_,
                                  "  ⚠️ leaves residue" if leftovers else ""))

covered = {os.path.basename(q)[len("probe-"):-3] for q in probes}


def stem(c):
    """The probe name a validator maps to. ⛔ `grade-block` is probed by
    `probe-grade`: the mapping is per validator, never a blind prefix strip."""
    return {"grade-block": "grade"}.get(c, c[len("check-"):])


missing = [c for c in checkers
           if stem(c) not in covered and stem(c) != "s"]
# ⭐ Not every probe covers a VALIDATOR. A hook has no findings of its own —
# what its probe proves is BEHAVIOUR — so counting it against the validator
# total reported "15 validators, 16 probes" and read as an inconsistency.
# ⛔ A hook may be a script in any language — looking only for `.sh` counted a
# python hook's probe against the VALIDATOR total and reported an inconsistency
# that was the counter's, not the tree's.
HOOKS = os.path.join(os.path.dirname(BIN), "hooks")
hook_probes = [q for q in probes
               if any(os.path.exists(os.path.join(HOOKS,
                       os.path.basename(q)[len("probe-"):-3] + ext))
                      for ext in (".sh", ".py"))]
# ── ⭐ THE SECOND QUESTION · is the tree clean RIGHT NOW ────────────────────
# 🔴 A probe answers "does this check detect what it claims?" — never "is the
# tree clean?" ⛔ The second question went unasked for seven audits while four
# unguarded calls sat in the code: every probe was green, and the validators
# they proved had never been run against the tree they live in.
#
# ⚠️ TWO QUESTIONS, TWO RUNS, REPORTED SEPARATELY. A suite that answers one and
# implies the other is worse than one answering neither, because it looks
# complete. This section never merges into the check count above: a probe result
# and a tree finding mean different things, and adding them would hide both.
#
# ⭐ `--quiet` is the uniform contract every validator honours: 0 clean,
# non-zero has findings. Because the contract is uniform this needs no knowledge
# of what any of them checks — which is what lets a new validator join with no
# edit here.
print("\n  ── the tree right now")
# ⭐ A validator that needs a SUBJECT is not run over the tree: with none given
# it prints its usage, and a usage banner is not a finding. ⛔ Reporting it as
# dirty is noise, and noise in the one section that says "something is wrong
# here" teaches the reader to skim it.
# ⚠️ Read from each tool's own `Usage:` line rather than listed here — a list
# goes stale the day somebody adds an argument.
def prints_usage(out):
    """⛔ A usage banner is not a finding.

    🔴 Three attempts to answer this by PARSING the usage text got it wrong
    three different ways: the first read only the first line and skipped a
    validator that sweeps; the second missed a form whose only extra token was
    an option. ⭐ The text describes the contract — running the tool MEASURES it,
    and this file exists because measuring beats reading.

    ⚠️ A tool that needs a subject answers by printing how to give it one. That
    is what is detected, because that is what actually happens.
    """
    head = "\n".join(out.strip().splitlines()[:3]).lower()
    return "usage" in head or head.startswith(("bin/", "grade-block"))


dirty, unmeasurable, skipped, mute = [], [], [], []
for c in checkers:
    try:
        rr = subprocess.run([sys.executable, os.path.join(BIN, c), "--quiet"],
                            cwd=ROOT, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        # ⬜ A validator that could not RUN is not a clean one. Reporting it as
        # passing is the exact shape of the failure this section exists for.
        unmeasurable.append((c, e.__class__.__name__))
        continue
    if rr.returncode == 0:
        # ⛔ CHK-TRV-002 · A CLEAN RUN MUST STILL SAY SO. ⚠️ Five validators
        # printed a summary line and then fell silent when their collection was
        # empty — and silence after a summary reads exactly like a tick to
        # anyone skimming a battery run, which is the false positive that rule
        # exists to stop.
        # ⭐ Checked on the VERBOSE run: `--quiet` is the exit code only, so the
        # quiet call above has no output to inspect by contract.
        try:
            plain = subprocess.run([sys.executable, os.path.join(BIN, c)],
                                   cwd=ROOT, capture_output=True, text=True,
                                   timeout=120)
        except (OSError, subprocess.SubprocessError) as e:
            unmeasurable.append((c, e.__class__.__name__))
            continue
        if not any(v in plain.stdout for v in ("✅", "🔴", "⚠️", "⬜")):
            mute.append(c)
        continue
    # ⭐ Measured, not parsed: a tool needing a subject says so by printing its
    # usage, and that is a SKIP — never a finding about the tree.
    # ⭐ CHK-QUI-001 · TWO CALLS, and that is the contract. `--quiet` answered
    # "is anything wrong"; only what said yes is asked again for the reason.
    # ⛔ Reading a reason out of a `--quiet` run is the third misreading of that
    # flag this engine has had, and each one looked correct until the contract
    # was honoured somewhere else.
    detail = subprocess.run([sys.executable, os.path.join(BIN, c)],
                            cwd=ROOT, capture_output=True, text=True,
                            timeout=120)
    if prints_usage(detail.stdout):
        skipped.append(c)
        continue
    # ⚠️ A FINDING OUTRANKS A GAP. Taking the first marked line printed a ⬜
    # "not measured" note above the 🔴 that made the validator exit non-zero —
    # the reader then sees a gap where there is a fault.
    lines = ([l for l in detail.stdout.splitlines() if "🔴" in l]
             or [l for l in detail.stdout.splitlines() if "🟡" in l]
             or [l for l in detail.stdout.splitlines() if "⬜" in l])
    first = (lines or detail.stdout.strip().splitlines() or ["(no output)"])[0]
    dirty.append((c, rr.returncode, first.strip()[:66]))

# ⬜ Said out loud, never counted as clean: a validator not run is one whose
# answer is unknown, and the difference from "clean" is the whole point.
for c in skipped:
    print("     ⬜ %s needs a subject · not run over the tree" % c)
if unmeasurable:
    for c, why in unmeasurable:
        print("     ⬜ NOT MEASURED · %s did not run (%s)" % (c, why))
if dirty:
    for c, code, first in dirty:
        print("     🔴 %s · exit %d · %s" % (c, code, first))
    print("     ⚠️ %d validator(s) report findings on THIS tree · the probes "
          "above say they WORK,\n"
          "        which is a different question and does not make these go "
          "away" % len(dirty))
else:
    print("     ✅ %d validator(s) run clean on this tree" % len(checkers))
if mute:
    # ⭐ Counted as failures: a validator whose verdict a reader cannot see has
    # not reported, whatever its exit code says.
    total += len(mute)
    failed += len(mute)
    for c in mute:
        print("     🔴 %s exits 0 and prints no verdict · ⛔ CHK-TRV-002 · "
              "silence reads as a pass" % c)

print("\n  ── coverage")
print("     validators: %d · with a probe: %d%s"
      % (len(checkers), len(probes) - len(hook_probes),
         " · + %d hook probe(s)" % len(hook_probes) if hook_probes else ""))
for c in missing:
    print("     ⬜ %s · NOT PROVEN — a validator with no probe is not demonstrated" % c)

_line = ("  ➜ checks: %d · failed: %d%s"
         % (total, failed, "" if not failed else "  🔴"))
print("\n" + _line)

# ⭐ The result is RECORDED where bin/generate-metrics can read it. ⛔ That
# generator used to run the battery to learn this number — which recursed
# (the battery runs the probe that exercises the generator) and cost a full
# verification run per read. ⚠️ A metric nobody can afford to regenerate is a
# stale number wearing a measured face.
try:
    _c = os.path.join(os.path.dirname(BIN), "cache")
    os.makedirs(_c, exist_ok=True)
    with open(os.path.join(_c, "last-battery.txt"), "w", encoding="utf-8") as _fh:
        # ⭐ THE DURATION TOO, and per probe. ⛔ Without it, comparing today
        # against a comment written when there were 14 probes is arithmetic
        # between different denominators — it reads as a 3.3× degradation and
        # is a 28% one. ⚠️ A total means nothing without its count.
        _fh.write(_line.strip() + "\n")
        _el = time.time() - _started
        _fh.write("seconds: %.1f · probes: %d · per_probe: %.2f\n"
                  % (_el, len(probes), _el / max(1, len(probes))))
except OSError:
    pass          # ⛔ recording the result never breaks the run that produced it
sys.exit(1 if failed or missing else 0)
