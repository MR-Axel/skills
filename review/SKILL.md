---
name: review
description: >
  Code review for security, performance and quality on a diff, with every finding
  anchored to a real file and line. Use before shipping. Use for: review this, code
  review, check my changes, /review.
license: MIT
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git status)
disable-model-invocation: true
---

# Code review

Review $ARGUMENTS, or the working diff if nothing was given (`git diff` for uncommitted,
`git diff <base>...HEAD` for a branch).

Read `.claude/project-profile.md` first for the stack, conventions and quality bar. Say so
if it is missing and review on general principles instead, noting that convention findings
will be weaker.

## Scope

**Review the diff, not the repository.** Pre-existing problems in untouched code are out
of scope, except where the diff makes one materially worse. If you find something serious
outside the diff, note it in one line at the end under `pre-existing`, and do not let it
crowd out the actual review.

## What to look for

### Security

- Secrets, keys, tokens or infrastructure identifiers committed in code or config.
- Untrusted input reaching a sink: HTML injection into the DOM, SQL built by string
  concatenation, shell commands built from user input, path traversal in file operations.
- Authorization checked on the server, not only hidden in the UI. A gate enforced only in
  the client is not a gate, and the network tab is right there.
- Row-level or record-level access rules present for any new table or column.
- Privileged credentials used only server-side, never shipped to the client bundle.
- Responses that return more fields than the caller needs, especially anything personal.

### Correctness

This is where real bugs live, and it deserves more attention than style.

- Unhandled promise rejections and swallowed errors.
- Off-by-one, boundary and empty-collection cases.
- State updated from stale values; race conditions between concurrent operations.
- Error paths that leave the system half-updated.
- Migrations that are not idempotent, or that lack a sensible default for existing rows.

### Performance

- Queries inside loops, when a single batched query would do.
- Selecting everything when two fields are needed; missing pagination on a set that grows.
- Expensive work repeated on every render or every request when it could be computed once.
- Unbounded growth: caches with no eviction, listeners never removed.

Judge this against the profile's stated performance constraints. Absent constraints,
flag only what is clearly quadratic or clearly unbounded, and skip micro-optimization.

### Quality

- Duplicated logic that the codebase already has a utility for.
- Convention drift from the profile or from neighbouring code.
- Type escapes (`any`, `@ts-ignore`, unchecked casts) beyond what the profile allows.
- Dead code left behind by the change.

## Evidence, not vibes

Every finding must name a **file and line that exists in the diff** and describe a concrete
failure: given this input or this state, this goes wrong. If you cannot write the failure
scenario, you do not have a finding, you have a preference. Drop it.

Do not pad the review. Three real findings beat fifteen with twelve stylistic
observations mixed in, because the twelve are what makes reviewers stop reading.

If the diff is genuinely clean, say so in one line. That is a valid and useful result.

## Output

```
[SEVERITY] path/to/file.ext:LINE, one-line claim
  Failure: <concrete input or state, and what goes wrong>
  Fix: <specific change>
```

`CRITICAL` data loss, security, or corruption. `HIGH` a bug users will hit. `MEDIUM`
maintainability or a bug in an unlikely path. `LOW` style and polish.

```
N findings (N critical, N high, N medium, N low)
Pre-existing (out of scope): <one line each, or none>
Verdict: APPROVE | APPROVE WITH NITS | REQUEST CHANGES
```

`REQUEST CHANGES` requires at least one critical or high finding. Do not block a change
over medium and low findings; list them and approve.
