#!/usr/bin/env bash
# remote-health.sh — runs ON THE SERVER as the forced command of the heartbeat key.
#
# ⭐ The heartbeat key can run THIS and nothing else (authorized_keys `command=`,
# no-pty, no forwarding). Read-only: it counts containers and asks the declared
# health endpoints. If the key ever leaks, all it grants is "are you alive?".
#
# Its two arguments are fixed INSIDE authorized_keys by `server install-key`,
# from target.conf — the client cannot change them:
#   $1  containers=<prefix>          only containers whose name contains it · "" = every one
#   $2  health=<name>:<port>:<path>  ask each matching container · "" = no HTTP check
#
# Prints ONE line, key=value, parsed by `connection/server/server`:
#   OK uptime=<s> running=<n> total=<n> health=<port>=<code>,… down=<names|-> unhealthy=<names|-> docker=<present|absent>
#
# ⛔ No fixed list of ports: they are read from what docker publishes for each
# container (`127.0.0.1:<host port>-><port>`), so a new one is measured the day it starts.
set -u
prefix="${1:-}"
hspec="${2:-}"
up=$(cut -d. -f1 /proc/uptime)
run=0; all=0; down=""; unh=""; health=""; dk=absent
if command -v docker >/dev/null 2>&1; then
  dk=present
  f=(); [ -n "$prefix" ] && f=(--filter "name=$prefix")
  run=$(docker ps "${f[@]}" --format x | wc -l)
  all=$(docker ps -a "${f[@]}" --format x | wc -l)
  down=$(docker ps -a "${f[@]}" --filter status=exited --filter status=dead \
         --filter status=restarting --format '{{.Names}}' | paste -sd, -)
  unh=$(docker ps "${f[@]}" --filter health=unhealthy --format '{{.Names}}' | paste -sd, -)
  if [ -n "$hspec" ]; then
    IFS=: read -r hname hport hpath <<< "$hspec"
    for port in $(docker ps --filter "name=$hname" --format '{{.Ports}}' \
                  | grep -oE "127\.0\.0\.1:[0-9]+->$hport" | cut -d: -f2 | cut -d- -f1 | sort -u); do
      code=$(curl -s -m 4 -o /dev/null -w '%{http_code}' "127.0.0.1:$port$hpath")
      health="$health,$port=$code"
    done
  fi
fi
echo "OK uptime=$up running=$run total=$all health=${health#,} down=${down:--} unhealthy=${unh:--} docker=$dk"
