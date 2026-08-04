---
name: project-setup
description: >
  Interviews you about a codebase and writes .claude/project-profile.md, the shared
  config that the dev, test, review, deep-review, ux, deploy, ship and product skills
  all read. Run once per repository. Use for: project setup, configure skills,
  set up my project, /project-setup.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Bash(git remote -v), Bash(git branch --show-current), Bash(cat package.json), Bash(ls *)
---

# Project setup

Writes `.claude/project-profile.md`: one file describing this codebase, read by every
other engineering skill in this collection. Without it those skills stop and point here,
rather than guessing your stack and generating code that does not match your conventions.

Run it once per repository. Re-run it when the stack changes.

## Why a shared profile

The alternative is each skill hardcoding a stack, paths and deploy commands. That works
for exactly one project and silently misfires on every other. One profile means the skills
stay generic and your project details live in your repo, where they belong and where you
can edit them without touching a skill.

## How to run it

**Detect first, then confirm. Never invent.**

Read what the repo already tells you before asking anything:

| Source | Tells you |
|--------|-----------|
| `package.json` | Scripts, framework, test runner, package manager |
| lockfile name | npm, pnpm, yarn or bun |
| `tsconfig.json` paths | Import aliases |
| top-level directories | Where source, tests and migrations live |
| `.github/workflows/` | The CI pipeline, which is the real build and test contract |
| config files (`vercel.json`, `supabase/`, `Dockerfile`, `fly.toml`) | Where it deploys |
| `README.md` | Everything the author thought worth saying |

Then present what you found and ask the user to confirm or correct it. A wrong detected
value that the user silently accepts is worse than a question, so show your evidence:
"found `npm run build` in package.json, is that the build command?" rather than a bare
prompt.

Ask only about what you could not detect. Three rounds, short.

### Round 1: stack and commands

Confirm the detected values, ask for what is missing:

- Framework and language, with versions if they matter to conventions
- Package manager
- Build command, test command, typecheck command, lint command
- Which of these are **required to pass before shipping**, and which are advisory
- Where the app is deployed, and the deploy command if there is one

If a command does not exist, record `none` rather than a plausible guess. A skill that
runs an invented command wastes a turn and reports a confusing failure.

### Round 2: conventions

- Directory layout: where pages, components, hooks, utilities, tests and migrations live
- Import alias, if any
- Files that must **never** be edited by hand (generated types, UI primitives from a
  component library, lockfiles, vendored code)
- Data access pattern: how the app talks to its backend, and where that client lives
- Error and notification pattern
- Auth pattern, if there is one

### Round 3: quality bar and deploy safety

- Definition of done: what has to be true before a change is considered finished
- Whether commits should be made automatically, or only with explicit approval
- Whether the skill may push, and to which branches it must never push directly
- Commit message convention, and any required trailer
- Design system basics if the project has one: theme, primary color, spacing scale,
  component library, icon set

**Ask about deploy permissions explicitly, and default to the cautious answer.** Deploying
and pushing are the only actions in this collection that touch something outside the
working tree. The user should say yes on purpose, not discover it afterwards.

## Secrets

**Never put a secret, key, token, connection string or project identifier in the profile.**

The profile is a file in the user's repository and is very likely committed. Anything that
identifies infrastructure belongs in an environment variable, and the profile should
reference the variable name, not the value.

This includes things that are not strictly secret but still map to live infrastructure:
project references, account IDs, deployment hooks, dashboard URLs. Write
`--project-ref "$SUPABASE_PROJECT_REF"`, never the literal ref. If the user offers one,
decline it and record the variable name instead.

Say this out loud once during the interview so the user does not paste one in.

## Output

Write `.claude/project-profile.md` from `assets/project-profile.template.md`, then show a
short summary and the list of skills now unlocked. Suggest adding the file to the repo so
the whole team gets the same behaviour, and warn that it should be reviewed for secrets
before the first commit.
