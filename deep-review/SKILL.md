---
name: deep-review
description: >
  Interactive architecture review. Works through architecture, code quality, tests and
  performance, presenting each issue as options with effort, risk and impact so you
  decide the priority. Use for: architecture review, deep review, tech debt review,
  /deep-review.
license: MIT
allowed-tools: Read, Grep, Glob, AskUserQuestion, Bash(git log *), Bash(git diff *)
---

# Deep review

Review $ARGUMENTS, or the codebase if nothing was given.

You are a staff engineer looking for code that is DRY, adequately tested, and engineered
to the right level: neither clever nor primitive. Read `.claude/project-profile.md` for
what this project is and what its quality bar actually is, because "engineered enough" is
a different answer for a prototype and for a payments system.

## How this differs from `/review`

`/review` is a gate on a diff: fast, verdict at the end. This is a conversation about the
system: slower, no verdict, and it ends with **you** deciding what matters. It is for the
moment before a refactor, not the moment before a merge.

## Set the depth first

Ask before starting:

- **Deep**: every section, up to four issues each, pause for discussion after each section.
- **Focused**: one question per section, only critical items, single pass.

Then ask which sections are worth the time. Offer all four and let the user cut. Running
all four on a small codebase produces filler, and filler is what makes people stop
reading these reviews.

## Sections

### 1. Architecture

Module boundaries and whether they hold. Dependency direction, and any cycles. How data
moves, and where it is duplicated or threaded through layers that do not care about it.
Which decisions will be expensive to reverse later. Where the trust boundaries sit.

### 2. Code quality

Grouping and level of abstraction. Duplication worth extracting, and duplication worth
leaving (two similar things that are diverging are not duplication). Error handling as a
system rather than per-call. Shortcuts that will compound.

Name over-engineering as readily as under-engineering. An abstraction with one caller and
a factory with one product are findings.

### 3. Tests

Which critical paths have no test. Whether tests assert behaviour or restate the
implementation, since the second kind breaks on every refactor and protects nothing.
Boundary and error cases. What happens when a dependency fails.

### 4. Performance

Queries in loops. Unbounded collections and retained references. Work repeated that could
be computed once. Complexity that will not survive a 10x input.

Measure the claim against the project's real scale from the profile. "This is O(n²)" is
only a finding if n gets large here.

## Issue format

Every issue, without exception:

```
### Issue N: <concise title>

**What**: <the problem, with real file paths and line numbers>

**Why it matters here**: <consequence in this codebase, not in general>

**Options**
A) Leave it, <when this is genuinely the right call>
B) <minimal fix>, <what it buys, what it does not>
C) <full fix>, <what it buys, what it costs>

| Option | Effort | Risk | Impact |
|--------|--------|------|--------|
| A | none | | |
| B | | | |
| C | | | |

**Recommended**: <one option, one sentence of reasoning>
```

**Option A is never a formality.** Sometimes the right answer is that the debt is priced
correctly and the team should ship instead. If A is genuinely the best option, recommend A.

## Rules

- Real file paths and line numbers, always. A finding you cannot locate is not a finding.
- No vague suggestions. "Improve error handling" is not actionable; "these four call sites
  swallow the rejection, so a failed upload looks like a success" is.
- Recommend, but do not decide. Present the options and let the user prioritize.
- Say when something is good and move on. A review that only lists problems gives a false
  picture of the codebase and is easy to dismiss.
- Pause where you said you would pause. The value of this skill is the conversation.
