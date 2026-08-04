---
name: deploy
description: >
  Run this repository's release pipeline: build, migrate, deploy, commit and push, using
  the commands and permissions in .claude/project-profile.md. Stops on the first failure
  and never pushes broken code. Use for: deploy, ship it, release, /deploy.
license: MIT
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: true
---

# Deploy

Read `.claude/project-profile.md` for the commands **and the permissions**. If it is
missing, stop: this skill runs commands that affect things outside the working tree, and
guessing them is not acceptable.

## Permissions come first

The profile records three separate answers. Honor each one, and when the profile does not
say, take the cautious reading and ask.

| Action | Default when unspecified |
|--------|--------------------------|
| Commit | Ask, showing the message first |
| Push | Ask, showing the branch and commit list |
| Deploy | Ask, showing the target |

Two hard rules that no profile setting overrides:

- **Never force-push, never rewrite published history, never push to a protected branch.**
  If the profile names branches that must not be pushed to directly and the current branch
  is one of them, stop and offer to create a branch instead.
- **Never deploy a build that did not pass.** There is no "the failure is unrelated"
  exception; if it is unrelated, it is still a red build going to production.

If secrets are needed for a step, they come from the environment. Never read a secret into
the transcript, never inline one into a command, never write one into a file.

## Pipeline

Stop at the first failure. Report where you stopped and what state things are in, which is
the part that matters when something breaks halfway.

### 1. Preflight

- `git status`: know what is uncommitted before touching anything.
- Confirm the current branch is one the profile allows.
- If the working tree has changes unrelated to this release, say so and ask. Sweeping up
  someone's half-finished work into a release commit is a bad surprise.

### 2. Validate

Run the profile's required checks (build, tests, typecheck). Anything the profile marks
required must pass. Report anything skipped.

### 3. Migrations

Only if the diff actually adds migration files. Apply with the profile's command.

Before applying, say what will run. A migration is the least reversible step in this
pipeline, and a one-line "about to apply 2 migrations: <names>" costs nothing and has
saved a lot of databases.

### 4. Server functions and assets

Only for functions the diff touched. Deploy each with the profile's command, using
environment variables for any project or account identifier.

### 5. Commit

- Stage **specific files**. Never `git add -A`: it is how secrets, scratch files and
  unrelated work get committed.
- Write the message in the profile's convention, and add the trailer the profile requires.
- Show the message and the file list, then commit according to the commit permission.

### 6. Push

Per the push permission. Show the branch and what will land.

### 7. Report

```
BRANCH:     <name>
VALIDATED:  build <status>, tests <status>, typecheck <status>
MIGRATIONS: N applied | none | skipped (<why>)
FUNCTIONS:  N deployed | none
COMMIT:     <hash> <subject> | not committed (<why>)
PUSH:       done | not pushed (<why>)
DEPLOY:     <target and status> | not deployed (<why>)
```

## When something fails

Report the failure, say clearly **what already happened and what did not**, and stop. Do
not retry a failed deploy in a loop, and do not work around a failing check to get the
pipeline green.

The dangerous state is a partial release: migrations applied but the code not shipped, or
functions deployed against an old schema. When you stop mid-pipeline, spell that out
first, before the error text, so the reader knows what they are dealing with.
