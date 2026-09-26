#!/usr/bin/env python3
"""probe-server — does the heartbeat name the RIGHT layer when each one fails?

⭐ WHAT IT MEASURES. `connection/server/server` exists to close one gap: from
the owner's machine «server down» and «tunnel down» looked identical (measured
2026-09-26 — the server had rebooted and nobody knew). A heartbeat that says
🔴 without saying WHICH layer is the same gap with a colour on it. Each case
stubs one layer — a local TCP port, a fake `ssh`, a fake `tailscale`, a fake
`docker` — and checks the verdict names it. ⛔ It never touches a real server.

⭐ AND THAT IT ASKS ONLY WHAT WAS DECLARED. A plain machine with no Docker, no
tunnel and no health endpoint must read 🟢 — never 🟡 for a service it does not run.

Exit: 0 every case behaves · 1 one does not
"""
import json, os, socket, subprocess, sys, tempfile, shutil, time
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

SERVER = os.path.join(ROOT, "connection", "server", "server")
REMOTE = os.path.join(ROOT, "connection", "server", "remote-health.sh")
results = []
WORK = tempfile.mkdtemp(prefix="mente-server-")
FULL = "tunnel=tailscale containers=app- health=agent:8788:/v1/health"


def case(label, ok, detail=""):
    print("  %-62s %s %s" % (label, "✅" if ok else "\U0001f534", detail))
    results.append((label, ok))


def stub(name, body):
    p = os.path.join(WORK, name)
    with open(p, "w") as fh:
        fh.write("#!/usr/bin/env bash\n" + body + "\n")
    os.chmod(p, 0o755)
    return p


OK_LINE = ("OK uptime=5000 running=28 total=28 health=8788=200,8798=200 down=- "
           "unhealthy=- docker=present")
PLAIN_LINE = "OK uptime=5000 running=0 total=0 health= down=- unhealthy=- docker=absent"
SSH_OK = stub("ssh-ok", 'echo "${STUB_LINE}"')
SSH_NO = stub("ssh-no", 'echo "Permission denied (publickey)." >&2; exit 255')
TS = stub("ts", 'case "$1" in status) printf "%b\\n" "${STUB_TS_STATUS}";; '
                'ping) [ "${STUB_TS_PING}" = pong ] && echo "pong from box" || exit 1;; esac')
# install-key stubs: every argv they receive is appended to a log, one call per line
LOG = os.path.join(WORK, "calls.log")
SSH_REC = stub("ssh-rec", 'printf "%%s\\n" "ssh $*" >> %s' % LOG)
SCP_REC = stub("scp-rec", 'printf "%%s\\n" "scp $*" >> %s' % LOG)

listener = socket.socket(); listener.bind(("127.0.0.1", 0)); listener.listen(8)
OPEN = listener.getsockname()[1]
# ⛔ A listener nobody accepts from fills its backlog: measured 2026-09-26, after
# ~13 beats the "open" port stopped answering and two cases read 🔴 network.
# ⭐ Accept and close, so the port stays open for every case.
import threading                                      # noqa: E402


def _drain():
    while True:
        try:
            c, _ = listener.accept()
            c.close()
        except OSError:
            return


threading.Thread(target=_drain, daemon=True).start()
s2 = socket.socket(); s2.bind(("127.0.0.1", 0)); CLOSED = s2.getsockname()[1]; s2.close()


def beat(port, ssh=SSH_OK, line=OK_LINE, ts_status="", ts_ping="", cmd="beat", state="s",
         extra=FULL, env_more=None):
    tgt = os.path.join(WORK, "target.conf")
    with open(tgt, "w") as fh:
        fh.write("host=127.0.0.1 user=probe name=box port=%d %s\n" % (port, extra))
    env = dict(os.environ, MENTE_SERVER_STATE=os.path.join(WORK, state),
               MENTE_SERVER_TARGET=tgt, MENTE_SERVER_SSH=ssh, MENTE_SERVER_TAILSCALE=TS,
               MENTE_SERVER_TCP_TIMEOUT="1", STUB_LINE=line,
               STUB_TS_STATUS=ts_status, STUB_TS_PING=ts_ping,
               MENTE_SERVER_KEY=os.path.join(WORK, "hb_key"))
    env.pop("SSHPASS", None)
    env.update(env_more or {})
    r = subprocess.run([sys.executable, SERVER] + cmd.split(), capture_output=True,
                       text=True, env=env, timeout=60)
    return r.returncode, r.stdout.strip()


try:
    print("═══ PROBE · server heartbeat ═══\n")
    rc, out = beat(OPEN)
    case("① every layer holds → 🟢", rc == 0 and out.startswith("🟢"), "rc %d" % rc)
    rc, out = beat(OPEN, line=OK_LINE.replace("8798=200", "8798=502"))
    case("② a declared health check ≠ 200 → 🟡 naming the port",
         rc == 2 and ":8798 → 502" in out, "rc %d" % rc)
    rc, out = beat(OPEN, line=OK_LINE.replace("down=-", "down=app-agent-1"))
    case("③ a container down → 🟡 naming it", rc == 2 and "app-agent-1" in out, "rc %d" % rc)
    rc, out = beat(OPEN, ssh=SSH_NO)
    case("④ the port answers, key refused → 🔴 key (the MONITOR is broken)",
         rc == 1 and " key " in out, "rc %d" % rc)
    rc, out = beat(CLOSED, ts_status="Logged out.")
    case("⑤ tunnel declared, not connected here → 🔴 tunnel",
         rc == 1 and " tunnel " in out, "rc %d" % rc)
    rc, out = beat(CLOSED, ts_status="100.64.0.9  box  u@  linux  -", ts_ping="pong")
    case("⑥ tailnet ping answers, port closed → 🔴 sshd", rc == 1 and " sshd " in out,
         "rc %d" % rc)
    rc, out = beat(CLOSED, ts_status="100.64.0.9  box  u@  linux  offline, last seen 2m ago")
    case("⑦ the tailnet sees it offline → 🔴 server OFFLINE",
         rc == 1 and " server " in out and "OFFLINE" in out, "rc %d" % rc)

    beat(OPEN, state="r")
    rc, out = beat(OPEN, line=OK_LINE.replace("uptime=5000", "uptime=120"), state="r")
    case("⑧ uptime went down between beats → REBOOTED, even in 🟢",
         rc == 0 and "REBOOTED" in out, "rc %d" % rc)
    rc, out = beat(OPEN, line=OK_LINE.replace("uptime=5000", "uptime=120"), state="r",
                   cmd="status --quiet")
    case("   … and --quiet still says it", "REBOOTED" in out, "said" if out else "SILENT")

    beat(OPEN, state="q")
    rc, out = beat(OPEN, cmd="status --quiet", state="q")
    case("⑨ status --quiet on a clean 🟢 → silent", rc == 0 and out == "",
         "silent" if not out else "spoke")
    p = os.path.join(WORK, "q", "last.json")
    d = json.load(open(p)); d["ts"] = int(time.time()) - 3600; json.dump(d, open(p, "w"))
    rc, out = beat(OPEN, cmd="status --quiet", state="q")
    case("⑩ no beat for an hour → ⬜ stale, the monitor stopped",
         rc == 3 and out.startswith("⬜"), "rc %d" % rc)
    rc, out = beat(OPEN, cmd="status", state="never")
    case("⑪ never measured → ⬜, not 🟢", rc == 3 and "never" in out, "rc %d" % rc)
    rc, out = beat(OPEN, line="", state="e")
    case("⑫ ssh answers but no OK line → 🔴 key, never 🟢", rc == 1, "rc %d" % rc)

    # ── ⭐ ONLY WHAT WAS DECLARED IS ASKED ───────────────────────────────────
    rc, out = beat(OPEN, line=PLAIN_LINE, extra="")
    case("⑬ a plain machine — no docker, no health, no tunnel → 🟢",
         rc == 0 and out.startswith("🟢"), "rc %d · %s" % (rc, out[:60]))
    rc, out = beat(OPEN, line=PLAIN_LINE, extra="containers=app-")
    case("⑭ containers declared, the server has no docker → 🟡 saying so",
         rc == 2 and "no docker" in out, "rc %d" % rc)
    rc, out = beat(CLOSED, extra="")
    case("⑮ no tunnel declared, port closed → 🔴 network, the layer NOT guessed",
         rc == 1 and " network " in out and "cannot be named" in out, "rc %d" % rc)
    rc, out = beat(OPEN)
    case("⑯ the label is the target's name=, never a hardcoded host",
         "server box" in out, out[:40])

    # ── ⭐ THE FORCED COMMAND CARRIES THE DECLARATION, FIXED AT INSTALL ──────
    open(os.path.join(WORK, "hb_key"), "w").write("k")
    open(os.path.join(WORK, "hb_key.pub"), "w").write("ssh-ed25519 AAAAzz mente-heartbeat")
    rc, out = beat(OPEN, cmd="install-key",
                   env_more={"MENTE_SERVER_SSH": SSH_REC, "MENTE_SERVER_SCP": SCP_REC})
    calls = open(LOG).read() if os.path.exists(LOG) else ""
    case("⑰ install-key bakes containers + health into the forced command",
         rc == 0 and "remote-health.sh app- agent:8788:/v1/health" in calls
         and "no-pty" in calls, "rc %d" % rc)
    case("   … with the owner's own key (BatchMode), no sshpass without SSHPASS",
         "BatchMode=yes" in calls and "sshpass" not in calls)

    # ── ⭐ remote-health.sh itself, against a fake docker ─────────────────────
    dlog = os.path.join(WORK, "docker.log")
    bindir = os.path.join(WORK, "bin"); os.makedirs(bindir)
    with open(os.path.join(bindir, "docker"), "w") as fh:
        fh.write('#!/usr/bin/env bash\nprintf "%%s\\n" "$*" >> %s\n' % dlog)
    os.chmod(os.path.join(bindir, "docker"), 0o755)
    env = dict(os.environ, PATH=bindir + os.pathsep + os.environ.get("PATH", ""))
    BASH = plat.bash()     # ⛔ never the bare name: on Windows it can resolve to WSL
    if not BASH:
        case("⑱ ⬜ remote-health · no usable bash here · NOT MEASURED", True)
    else:
        r = subprocess.run(list(BASH) + [REMOTE, "app-", ""], capture_output=True, text=True,
                           env=env, timeout=30)
        dl = open(dlog).read() if os.path.exists(dlog) else ""
        case("⑱ remote-health filters by the declared prefix",
             r.stdout.startswith("OK ") and "--filter name=app-" in dl
             and "docker=present" in r.stdout, r.stdout.strip()[:60])
    env2 = dict(os.environ, PATH="/usr/bin:/bin")
    has_docker = shutil.which("docker", path="/usr/bin:/bin")
    if has_docker or not BASH:
        case("⑲ ⬜ no docker → docker=absent · NOT MEASURED, docker is installed here", True)
    else:
        r = subprocess.run(list(BASH) + [REMOTE, "", ""], capture_output=True, text=True,
                           env=env2, timeout=30)
        case("⑲ no docker on the server → one OK line, docker=absent",
             r.stdout.startswith("OK ") and "docker=absent" in r.stdout, r.stdout.strip()[:60])
finally:
    listener.close()
    shutil.rmtree(WORK, ignore_errors=True)

sys.exit(report(results))
