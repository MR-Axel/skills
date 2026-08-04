---
name: dev
description: >
  Implement a feature or fix a bug following this repository's own conventions, read from
  .claude/project-profile.md rather than assumed. Use for: implement, build a feature,
  fix this bug, add support for, /dev.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Development

Implement: $ARGUMENTS

## Before anything

Read `.claude/project-profile.md`. It holds the stack, layout, conventions, and the list
of files that must never be hand-edited.

**If it does not exist, stop and say so:** "No project profile found. Run `/project-setup`
first, or tell me the stack and I will work from that for this one task." Do not infer a
stack from a couple of file extensions and start writing: guessed conventions produce code
that looks plausible, passes review, and is wrong for this codebase.

## The loop

### 1. Read before writing

Find the closest existing thing to what you are about to build and read it. Not one file:
the pattern. If you are adding a hook, read three hooks. If you are adding a route, read
how routes are registered and how the neighbouring ones handle loading and errors.

The goal is that your diff is indistinguishable from code the team wrote. Matching the
surrounding style is not cosmetic, it is what makes the change reviewable.

### 2. Plan, proportionally

For a one-line fix, skip this. For anything touching three or more files, or any schema
change, write the checklist first: files, data changes, migrations, tests. If the plan
turns out to be wrong halfway through, stop and re-plan rather than pushing through with
an approach you have already stopped believing in.

### 3. Implement

- Minimum code that satisfies the requirement. No speculative abstraction, no options
  nobody asked for.
- Follow the profile's conventions exactly, including naming and file placement.
- Never hand-edit anything on the profile's do-not-edit list.
- Never hardcode a secret, key, token or infrastructure identifier. Environment variables,
  always, and if one is needed that does not exist yet, say so rather than inlining a value.
- Handle the unhappy paths the surrounding code handles: loading, empty, error. A feature
  that only works on the happy path is not done.

### 4. Fix the cause, not the symptom

Given a bug, find why it happens before changing anything. A guard that suppresses a
symptom is a second bug wearing the first one's clothes. If the real fix is out of scope,
implement the narrow fix and **say explicitly** that it is a patch and what the underlying
problem is.

### 5. Verify, then report honestly

Run the profile's build and test commands. Then read your own diff as if reviewing someone
else's PR.

Report what actually happened. If tests fail, say they fail and paste the output. If you
skipped something, say which and why. If you are unsure a change is correct, say that
instead of asserting success. A confident wrong report costs far more than an honest
uncertain one.

## Scope discipline

Do what was asked. If you spot something else worth fixing, mention it in one line at the
end rather than fixing it inside this change: an unrelated fix buried in a feature diff is
how review misses things.

If the request is ambiguous in a way that changes the work materially, ask. If it is
ambiguous in a way a careful colleague would just decide, decide and state the assumption.

## Report

```
CHANGED: <files>
APPROACH: <one or two sentences>
BUILD: pass | fail | not run (<why>)
TESTS: pass | fail | not run (<why>)
ASSUMPTIONS: <anything decided rather than asked>
NOT DONE: <anything in scope that was left out, and why>
NOTICED: <out-of-scope issues, one line each, not fixed>
```
