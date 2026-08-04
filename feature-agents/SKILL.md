---
name: feature-agents
description: >
  Runs a feature through five specialist subagents instead of one context: spec, planner,
  tester, QA, deployer. Each gets only the tools its job needs, so the spec writer
  physically cannot write code and the planner physically cannot run commands. For changes
  big enough that phase discipline stops holding on its own. Use for: delegar por fases,
  subagentes, agentes especializados, spec agent, planner agent, /feature-agents, no
  empieces a codear todavia, quiero el plan antes de tocar codigo.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Feature agents

A delegation layer for a feature: five subagents, each with the tools its job needs and
nothing else.

Read `.claude/project-profile.md` first. If it is missing, stop and point at
`/project-setup`. These agents plan against your conventions, and a plan built on a guessed
stack is a plan you will throw away.

## When to use this instead of `/ship`

`ship` runs the same delivery arc in one context, and for most changes that is the right
call: less overhead, less handoff, one continuous train of thought.

Reach for this one when the change is big enough that **phase discipline stops holding on
its own**. In a single context the pull toward writing code while still working out the
requirements is strong, and what comes out is a plan reverse engineered from a half finished
implementation.

Delegation makes that structurally impossible. The spec writer has `Read, Grep, Glob,
AskUserQuestion` and cannot write a file. The planner cannot run bash. The QA agent cannot
push. The boundary is not a promise in a prompt, it is the tool list.

Rough line: three or more files, a schema change, an integration, or anything where being
wrong is expensive. Below that, `ship`.

## The five

| Agent | Gets | Cannot |
|---|---|---|
| `feature-spec` | Read, Grep, Glob, AskUserQuestion | write anything, propose architecture |
| `feature-planner` | Read, Grep, Glob | write, run commands |
| `feature-tester` | Read, Write, Edit, Bash, Grep, Glob | set up test infra that did not exist |
| `feature-qa` | Read, Grep, Glob, Bash | edit source, push |
| `feature-deployer` | Read, Bash, Grep | run without an explicit human yes |

They install into `.claude/agents/` (see the README). In the repo on purpose: useful agents
know your conventions, and conventions are per repo.

## The flow

```
spec ─▶ plan ─▶ implement ─▶ test ─▶ QA ─▶ human check ─▶ deploy
```

**1 · Spec.** Call `feature-spec` with the request. It returns acceptance criteria that can
be checked pass or fail, plus the open questions asked in a single batch. If more than two
big assumptions are still unresolved when it finishes, ask before planning.

**2 · Plan.** Enter plan mode, call `feature-planner` with the spec, show the result, wait
for approval. If the user says "just do it" without looking, show the plan anyway. Ten
seconds of reading against an afternoon of rework is not a close trade.

**3 · Implement.** Follow the plan, one commit per step. Use `dev` for the actual writing if
you have it installed. If you discover the plan was wrong, **go back to step 2**. Pouring
code onto a broken plan is how you end up with a feature that works and a codebase that does
not.

**4 · Test.** Call `feature-tester` with the diff. For a bug fix, the test has to be seen
red against the old code before it can be trusted green against the fix.

**5 · QA.** Call `feature-qa`. It verifies against **the spec**, not against what got built.
Checking that the code does what the code does is free and worthless.

**6 · Human check.** The person who owns the product tries it on their machine. Wait for an
explicit yes. Silence is not approval.

**7 · Deploy.** Call `feature-deployer`, which refuses without step 6. If you use the
`deploy` skill for the release itself, this agent is the wrapper that checks the
preconditions and verifies afterwards.

## What each handoff carries

Pass three things: the original request, the previous phase's output, and the constraints
specific to this work.

The thing that most often goes wrong here is **summarising the previous output instead of
passing it**. A spec compressed into three bullets loses exactly the constraint the planner
needed, and nobody notices until the plan comes back missing it.

## Incident memory

The planner reads `.claude/memory/incidents.md` before planning: the traps this repo already
sprung, so it warns you before you walk into one again.

This is the piece that makes the kit improve instead of repeat. See
[`references/incident-memory.md`](references/incident-memory.md) for the format and, more
importantly, for what does not belong in it.

## When not to delegate

| Scope | Worth it |
|---|---|
| Typo, copy, comment | no |
| One file, one new branch | no, use `dev` |
| Small feature, 1 to 3 files | usually not, use `ship` |
| Medium feature, new area | yes |
| Large feature, migration, integration | yes, all five |

Delegation costs context and handoffs. On a small change that overhead buys nothing, and a
process nobody believes in is a process people route around.
