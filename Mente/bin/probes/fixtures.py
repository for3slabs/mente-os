#!/usr/bin/env python3
"""Fixtures the probes plant. ⭐ Every one carries the probe marker in its
IDENTITY, not only in its folder name: a fixture whose declared id differs
from what other fixtures point at makes a working graph check read as broken.
"""
import datetime, os
from harness import MARK, ROOT

TODAY = datetime.date.today().isoformat()
BLOCKS = os.path.join(ROOT, "work", "blocks")


def block_text(bid, scope="", conn="- none", fric="- none", status="active",
               lane="task", extra=""):
    return """# BLOCK · %(id)s

## A · Identity

id: %(id)s
type: docs
intent: a fixture used to prove a check detects what it claims
status: %(status)s
lane: %(lane)s
owner: someone
created: %(d)s · updated: %(d)s

## B · Scope

### ✅ IN
- this file
%(scope)s

### ⛔ OUT
- DO NOT touch anything else · DERIVED: another block owns it

### 🔒 INVARIANTS
- the fixture stays readable

## C · Connections

%(conn)s

## D · Required standards

- `rules/contract-block.md`

## E · State

current: writing
next: verify
blockers: none
updated: %(d)s

## H · Friction log

%(fric)s
%(extra)s""" % {"id": bid, "scope": scope, "conn": conn, "fric": fric,
                "status": status, "lane": lane, "d": TODAY, "extra": extra}


def block(probe, name, record=True, **kw):
    """Plant a block whose declared id EQUALS what dependencies point at.

    ⭐ A CLOSED block gets its close.json, because BLK-CLS-007 requires one and
    a fixture must be valid except for the defect under test — ⛔ otherwise
    every closing case fails twice and the second finding is the fixture's own.
    ⚠️ `record=False` is for the cases that test the record's absence.
    """
    bid = MARK + "-" + name
    d = probe.track(os.path.join(BLOCKS, bid))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(
        block_text(bid, **kw))
    if record and kw.get("status") == "closed":
        open(os.path.join(d, "close.json"), "w", encoding="utf-8").write(
            '{"block": "%s", "verdict": "MVP", "dimensions": '
            '{"architecture": "undeclared"}}' % bid)
    return bid
