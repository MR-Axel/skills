# Project profile

<!--
Written by /project-setup. Read by: dev, test, review, deep-review, ux, deploy, ship,
product. Edit by hand any time.

NEVER put a secret, key, token, connection string or infrastructure identifier in this
file. It lives in the repo and will be committed. Reference environment variable names
instead: "$SUPABASE_PROJECT_REF", not the ref itself.
-->

Project: <name>
What it does: <one sentence, so a review skill knows what "correct" means here>
Last updated: YYYY-MM-DD

## Stack

| Layer | Choice |
|-------|--------|
| Language | |
| Framework | |
| Styling | |
| Component library | |
| Icons | |
| State and data fetching | |
| Backend / database | |
| Auth | |
| Hosting | |
| Package manager | |

## Commands

| Purpose | Command | Required to pass before shipping? |
|---------|---------|:---------------------------------:|
| Install | | |
| Build | | yes |
| Test | | |
| Typecheck | | |
| Lint | | |
| Migrations | | |
| Deploy | | |

Use `none` where a command does not exist. Do not guess.

Commands that need an environment variable (record the variable name, never the value):
-

## Layout

| What | Where |
|------|-------|
| Source root | |
| Pages / routes | |
| Components | |
| Hooks / composables | |
| Utilities | |
| Tests | |
| Migrations | |
| Server functions | |
| Types | |

Import alias:

**Never edit by hand** (generated, vendored, or owned by a library):
-

## Conventions

Data access pattern:
Error handling and user notification pattern:
Auth pattern:
Naming conventions worth stating:

Anything a newcomer gets wrong on their first PR:

## Design system

Theme:
Primary color:
Background / surface tokens:
Typography scale:
Spacing and radius conventions:
Section header pattern:
Icon sizing convention:

Leave blank if the project has no design system; the `ux` skill will fall back to generic
accessibility and responsiveness checks and will say so.

## Quality bar

Definition of done:
-

Test coverage expectation:
Performance constraints that matter here:
Accessibility target (for example WCAG 2.1 AA):

## Git and deploy safety

| Question | Answer |
|----------|--------|
| May skills commit automatically? | ask-first / yes |
| May skills push? | no / yes |
| Branches that must never be pushed to directly | |
| Commit message convention | |
| Required commit trailer | |
| May skills deploy? | no / ask-first / yes |
| Deploy target | |

## Product context

<!-- Used by the `product` skill. Describe your own model. Nothing here is required. -->

Who the users are:
How the product makes money (if it does):
Tiers or plans, and what separates them:
The conversions or actions that matter:
Metrics this project actually tracks:
