# connection/server/ — knowing your server is alive while nobody uses it

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ the code travels; ⛔ `target.conf` and `state/` are INSTANCE and never do

---

## Purpose

One question, answered every five minutes without a session, a model or a person: **is the
server still alive — and if not, which layer failed?** The answer is read at session start in
milliseconds, from disk, with no network.

> ⭐ **Why it exists** (measured 2026-09-26 on a real installation): the server stopped answering
> SSH and HTTP, and from the owner's machine "server down" and "tunnel down" looked identical.
> Logged in minutes later it said `up 11 minutes` — it had rebooted, and nobody knew.
> ⛔ A server you only check when you use it is a server whose outages you never hear about.

---

## Set it up — three commands, once

```
1. write connection/server/target.conf       one line, see below
2. connection/server/server install-key      a dedicated key that can ONLY ask "are you alive?"
3. connection/server/server timer on         a beat every 5 min from cron
```

`install-key` uses **your own SSH key** when you have one; only if that is refused does it need
`SSHPASS` for that single step. ⭐ After it, nothing needs your credential again: the heartbeat key
is locked in `authorized_keys` to `remote-health.sh` — no shell, no forwarding, read-only.

### `target.conf`

| Key | Needed | What it does |
|---|---|---|
| `host` `user` `name` | ✅ | where to connect, as whom, and the label the verdict prints |
| `port` | — | SSH port · default 22 |
| `containers` | — | only containers whose name contains it · default: every one |
| `health` | — | `<name>:<port>:<path>` · ask each matching container on that path · default: no HTTP check |
| `tunnel` | — | `tailscale` · lets a 🔴 name the layer · default: none |

⭐ **Only what is declared is asked.** A plain machine with no Docker, no tunnel and no health
endpoint reads 🟢 — never 🟡 for a service it does not run. And with no tunnel declared, an
unreachable server is 🔴 `network` with the words *"the failing layer cannot be named"*: guessing
"server down" would be the exact confusion this folder exists to end.

---

## Reading the verdict

| | Layer | Means |
|---|---|---|
| 🔴 | `tunnel` | the declared tunnel is not connected on THIS machine |
| 🔴 | `server` | the tunnel sees it offline, or it does not answer a ping |
| 🔴 | `sshd` | it answers the tunnel ping, but the SSH port is closed |
| 🔴 | `network` | the port is closed and no tunnel is declared to say why |
| 🔴 | `key` | the port answers but the heartbeat key is refused — **the monitor is broken** |
| 🟡 | `service` | up, but a container is down or unhealthy, or a declared health check ≠ 200 |
| 🟢 | `ok` | every declared layer holds |
| ⬜ | stale | no beat for three intervals — the monitor itself stopped |

A reboot between two beats is reported even in 🟢. `server status` is silent when all is green.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| the heartbeat and the one script its key may run | your credential — that is `secrets/`, and the heartbeat key lives there too |
| `target.conf` — this machine's fact, gitignored | the server's own code or data |
| `state/` — the last verdict and a week of beats | anything that needs a model or a session to run |

---

Related: `../README.md` (the outward door) · `server` (the heartbeat, its docstring is the
reference) · `remote-health.sh` (the only thing the key may run) · `../../hooks/session-start.sh`
(reads the last verdict at startup) · `../../secrets/README.md` (where the key lives).
