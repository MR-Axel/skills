---
name: ship
description: >
  Full delivery pipeline for one feature: plan, implement, validate, self-review, product
  check, then deploy with your approval. Chains the dev, test, review, product and deploy
  skills. Use for: ship this feature, end to end, full pipeline, /ship.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
disable-model-invocation: true
---

# Ship

Deliver end to end: $ARGUMENTS

Read `.claude/project-profile.md` first. If it is missing, stop and point at
`/project-setup`. This pipeline ends in a deploy, and a deploy driven by a guessed
configuration is not something to attempt.

## Stages

Each stage is the corresponding skill's job. Follow those files rather than duplicating
their rules here, and do not skip a stage because the change looks small: the pipeline is
the point, and small changes are exactly the ones that ship broken.

### 0. Plan

List what will change: files, data, migrations, tests. For anything touching three or more
files or any schema, think the approach through before writing code.

Show the plan and get a go-ahead when the change is substantial. For a small fix, state
the plan in two lines and continue.

### 1. Implement, see `dev`

Read the surrounding code, match its conventions, handle the unhappy paths.

If the approach turns out to be wrong mid-implementation, **stop and re-plan**. Pushing
through an approach you have stopped believing in produces the changes that are hardest to
review and hardest to undo.

### 2. Validate, see `test`

Run the profile's required checks. Fix what fails and re-run. Do not continue with a
failing required check, and do not reclassify a failure as unrelated to get past it.

### 3. Self-review, see `review`

Review your own diff as if someone else wrote it. Fix critical and high findings before
continuing. List medium and low findings in the final report rather than fixing them
silently.

Then the question that catches the most: **is there a simpler version of this change?**
Ask it once, honestly. If yes and the rewrite is cheap, do it. If yes and it is expensive,
say so in the report rather than pretending you did not notice.

### 4. Product check, see `product`

Only if the profile has a product context section. Does the change actually serve the
user need behind the request, are the states complete, is it discoverable?

### 5. Deploy, see `deploy`

Honor the profile's commit, push and deploy permissions. **Ask before the first
irreversible step** unless the profile has already granted it. Approval for one stage is
not approval for the next.

### 6. Record what went wrong

If anything in this pipeline needed correcting, append to `.claude/lessons.md`:

```
## YYYY-MM-DD, <feature>
**What happened**: <the mistake>
**Root cause**: <why>
**Rule**: <what to do differently>
```

Only real corrections. A lessons file padded with "remembered to run the build" stops
being read, and then the real entries go unread too.

Read this file at the start of the next `/ship`.

## Report

```
FEATURE:    <what was built>
PLAN:       <followed | re-planned at stage N because ...>
FILES:      N changed
VALIDATION: build <status>, tests <status>, typecheck <status>
REVIEW:     N critical, N high (fixed), N medium, N low (listed below)
PRODUCT:    <ok | gaps | n/a>
DEPLOY:     <status, or not deployed and why>
LESSONS:    <new entries, or none>
STATUS:     SHIPPED | STOPPED AT <stage>
```

`SHIPPED` only when it actually shipped. If the pipeline stopped, say where and what state
things are in. A pipeline that reports success it did not achieve is worse than no
pipeline, because the next person builds on top of it.
