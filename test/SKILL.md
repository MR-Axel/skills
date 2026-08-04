---
name: test
description: >
  Run this repository's validation pipeline (tests, build, typecheck, lint) from the
  commands in .claude/project-profile.md and report honestly what passed, failed and was
  skipped. Use after code changes. Use for: validate, run tests, check the build, /test.
license: MIT
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: true
---

# Test and validate

Read `.claude/project-profile.md` for the command list. If it is missing, stop and say
`/project-setup` has not been run; offer to detect the commands from `package.json` for
this one run.

## Run order

Cheapest and most informative first, so a broken typecheck does not wait behind a five
minute test suite.

1. **Typecheck**
2. **Lint**
3. **Tests**
4. **Build**

Run every check even if an early one fails, unless a failure makes a later one
meaningless (a failed install makes everything meaningless; a lint error does not). One
run should tell the user everything that is wrong, not just the first thing.

Where the profile marks a command `none`, **skip it and report it as skipped**. Do not
substitute a command you think probably exists.

## Beyond the commands

The commands catch what they were written to catch. These are the gaps worth a look on
changed files only, not the whole repo:

- **Unused imports and dead variables** left behind by a refactor, if lint does not
  already cover it.
- **Schema drift**: a migration added without the generated types regenerated, or an enum
  value added in application code with no corresponding migration. The profile says where
  migrations and generated types live.
- **Registration gaps**: a new page, route, command or handler that was created but never
  wired into wherever the project registers them.
- **Server functions**: created or modified without the error handling and headers that
  the neighbouring ones have.

Check these only when the diff touches the relevant area. Say `n/a` otherwise rather than
inventing a finding.

## Reporting

Honesty is the entire product of this skill. The user is about to decide whether to ship
based on this table.

```
TYPECHECK: pass | fail | skipped (<reason>)
LINT:      pass | fail | skipped (<reason>)
TESTS:     pass (N) | fail (N of M) | skipped (<reason>)
BUILD:     pass | fail | skipped (<reason>)

Extra checks:
IMPORTS:   pass | N issues | n/a
SCHEMA:    pass | N issues | n/a
WIRING:    pass | N issues | n/a
```

Rules:

- **Never report a check as passing if it did not run.** `skipped` is a valid, useful
  answer. A green table that quietly omits the suite that would have failed is the worst
  output this skill can produce.
- **Paste the actual failure output**, trimmed to the relevant lines, with file and line.
  A summary of an error is not an error.
- **Warnings are not failures.** Say which warnings appeared and that they are warnings.
- End with one line: `READY TO SHIP` only when everything required by the profile passed,
  otherwise `NOT READY: <the blocking items>`.
