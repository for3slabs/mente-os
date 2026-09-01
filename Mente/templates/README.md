# templates/ — the blueprints `bin/init` stamps into a new instance

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}} · **Scope:** ⚠️ ENGINE — travels with the repo.

## What this folder is

Every file here ends in `.template`. It is a **blueprint**, not a live file. `bin/init` copies
each one into its real location, fills the placeholders, and asks the user for whatever is
missing. The generated copies (`CLAUDE.md`, `PROJECT-RULES.md`, `mente.config.yml`,
⬜ `docs/WORKSPACE.md` (created at install), and the architecture pillar) are **instance files** — they are gitignored
and never travel between clones.

> ⭐ **The whole point:** a fresh clone owns nothing personal. Identity, repos, and project state
> enter **once**, through `bin/init`, from the user in front of it — never baked into a file that
> shipped from someone else's machine.

## ⛔ The one rule that must never break

**A template must not contain instance data.** No real name, no email, no real repo or org name,
no machine path, no product state, no dated incident, no secret of any kind.

> 🔴 **Why, measured:** when `mente.config.yml` travelled with a real owner name inside, `bin/init`
> on someone else's clone **never asked** for the owner — it found the name already written and
> took it as truth. A personal value disguised as an engine default. The same failure hit
> `PROJECT-RULES.md` (it shipped with 11 mentions of the previous owner and zero of the real one).
> A template that carries instance data turns the installer into a leak.

If you ever find a real value in a template, that is a bug — remove it and replace it with the
right shape below.

## How a value enters — three shapes, pick the right one

| The content is… | How it must appear in the template | Example |
|---|---|---|
| **Engine doctrine** — a rule, the philosophy, the structure. Same for everyone. | Written out in full. Never a placeholder, never a blank. | the rule-inheritance diagram, the code-vs-document law |
| **Identity** — a single value `bin/init` substitutes. | A `{{placeholder}}` in lowercase. | `{{owner}}` · `{{project}}` · `{{date}}` |
| **A declaration only the user can make** — repos, gates, project state, pillars. May be zero, one, or many. | A `⬜` marker: an EMPTY default plus a comment saying what to put and a commented example to copy. **Never a pre-filled example that reads as done.** | `gates: []` with a commented shape above it |

⭐ **One template breaks the "born empty" rule on purpose: `pieces.tsv.template`.** It ships with
the engine's rows because a structure check with an empty table verifies nothing and stays silent
about every piece that disappears. ⚠️ It is therefore the one template that must be updated
whenever a piece is added to the engine — and the only one where "empty" would be the bug.

> ⭐ **The model file is `WORKSPACE.md.template`** — it is almost all ⬜ markers, because almost
> all of its content is the user's to declare. Read it before writing or editing any template.

## Why ⬜ and not a filled-in example

A pre-filled example (`siblings: my-app`) is dangerous: a user in a hurry reads it as "already
configured" and leaves it. `my-app` does not exist on their machine, so the guard aimed at it
**fails silently** — a green light that protects nothing. A `⬜` empty default (`siblings: []`)
cannot be mistaken for done: it announces what is missing. The example still lives right there,
**in a comment**, so the user sees the shape without inheriting a fake value.

## The placeholders `bin/init` fills

| Placeholder | Becomes | Source |
|---|---|---|
| `{{owner}}` | the owner's name | `owner.name` in `mente.config.yml`, asked on init |
| `{{project}}` | the project name | derived on init |
| `{{date}}` | the generation date | the day `bin/init` runs |

⚠️ Placeholders are **case-sensitive** and must match exactly what `bin/init` looks for. Use the
same form (lowercase `{{owner}}`) across every template, or the substitution silently leaves the
literal text behind.

## The files here

| Template | Generates | Notes |
|---|---|---|
| `CLAUDE.md.template` | `CLAUDE.md` | the router. Mostly doctrine; the § ESTADO block is the only ⬜ zone. Points at the architecture pillar via config, never by filename |
| `PROJECT-RULES.md.template` | `PROJECT-RULES.md` | project rules. Doctrine + a ⬜ scope zone and a ⬜ repos zone. §5 carries no security values — WHERE, never WHAT |
| `mente.config.yml.template` | `mente.config.yml` | the instance declaration. Mostly ⬜: `owner`, `pillars`, `gates`, `siblings`. `gates`/`siblings` default to `[]` and take zero, one, or many entries |
| `WORKSPACE.md.template` | ⬜ `docs/WORKSPACE.md` (created at install) | ⭐ the model — almost all ⬜. Carries no values: says WHERE a secret lives, never WHAT |
| `ARCHITECTURE.md.template` | the architecture pillar (path declared in `mente.config.yml` → `pillars.architecture`) | born empty; the user fills it as the project takes shape. Form-agnostic — declares components, invariants, limits and load-bearing decisions without imposing a shape |
| `pieces.tsv.template` | `pieces.tsv` | ⚠️ **the one template that ships with content**: the engine's own rows. It cannot be born empty — without them `check-structure` has nothing to verify |
| `RESUME.md.template` | ⬜ `memory/RESUME.md` (created at install) | the cold-start brief. Born empty, but carries the explanation of the cycle: you never write it by hand, the closing routine does |
| `PENDING.md.template` | ⬜ `memory/PENDING.md` | the debt list. Born empty; carries the entry shape and the rotation rule |
| `bridges.md.template` | `connection/bridges/` | the registry of other installations. Born with **no entries** — nobody inherits somebody else's neighbours |

## The pillar circuit — how the architecture source of truth is wired

No file hardcodes the architecture filename. It travels through config:

```
mente.config.yml  →  pillars.architecture: <path>   (the user points here once the file exists)
        ▲                        │
        │ generated from         │ read by
        │                        ▼
ARCHITECTURE.md.template   CLAUDE.md + PROJECT-RULES.md   ("the architecture pillar declared in config")
```

Start from `ARCHITECTURE.md.template`, fill it in, then point `pillars.architecture` at it. Until
it exists, `pillars.architecture` stays `null`.

## ⚠️ Keep templates in sync with the live files

A template that lags behind the engine is worse than no template: `bin/init --force` would
**downgrade** a working clone by generating an older file that the current checks reject. If you
change a rule in the engine, update its template in the same commit.

---

Related: `bin/init` (what stamps these) · `mente.config.yml.template` (the declaration) ·
`../.gitignore` (why the generated copies never travel) · `../rules/rule-config-hygiene.md`.