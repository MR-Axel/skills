---
name: decision-log
description: >
  Keeps a living log of the non obvious development decisions, the ones you cannot recover
  by reading the code or the git history: why this model, why this limit, why this approach
  and not the other one. Writes the entry in the same commit that implements the decision,
  and reads the log before proposing something that contradicts one. Use for: por que
  hicimos esto asi, decision log, ADR, architecture decision, documentar una decision,
  DECISIONS.md, /decision-log, esto ya lo habiamos decidido.
license: MIT
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(git log*), Bash(git diff*)
---

# Decision log

One file at the repo root, `DECISIONS.md`, with the development decisions that are **not
recoverable by reading the code**.

Not a changelog. Git already tells you what changed and when, and it does it better than any
file a human maintains. What git does not tell you is why the cap is 500 and not 1000, why
this model and not the cheaper one, why this approach after the other one was tried and
abandoned.

That reasoning lives in someone's head, and it leaves when they do. Six months later
somebody sees a number with no explanation, assumes it was arbitrary, and changes it. The
outage that follows is the cost of not having written one paragraph.

## When to write an entry

When you make a decision that **someone could reasonably question later**, and the answer is
not visible in the diff.

Concretely:

- A limit, a threshold, a timeout, a cap. Any number that is not obvious.
- Choosing between two viable approaches, when the loser was genuinely viable.
- A constraint that comes from outside the code (a platform limit, a provider's pricing, a
  legal requirement, an ops decision).
- Something deliberately **not** done, and why. This is the one people skip and the one that
  saves the most time: without it, the next person spends a day building what you already
  ruled out.
- A workaround for someone else's bug, with what it works around. Otherwise it looks like
  clutter and gets cleaned up.

## When not to

- The code explains it. If a reader can see why by reading the function, an entry is noise.
- It is a preference with no consequence. Naming, formatting, ordering.
- It only matters inside one conversation.

The log is only useful while it can be read end to end. A log with everything in it stops
being read, which is the same as not having one.

## Format

Newest on top. One entry per decision.

```markdown
## <date> · <what was decided, in one line>

The context in one or two sentences: what was going on that forced a decision.

**Decision**: what you chose.

**Why**: the reasoning. The part that is not in the code.

**What was rejected**: the other option and why it lost. If there was no alternative, say
that instead; "there was nothing else" is also information.

**What would change this**: the condition that would make it worth revisiting. Optional,
but it turns a decision into something reviewable rather than permanent by accident.
```

Write the **why** for someone who does not have your context and is not going to ask you.
That person is often you, later.

## The rule that makes it work

**The entry goes in the same commit that implements the decision.**

Not afterwards. Afterwards is a documentation task, documentation tasks get deprioritised,
and a decision log that lags behind the code is worse than none: it describes a system that
no longer exists and people trust it anyway.

If the decision is worth an entry, the entry is part of the work. Same commit, or it did not
happen.

## Reading it

Before proposing something that touches an existing decision, **read the log**.

This is half the value and the half that gets forgotten. A log nobody reads is a diary. The
moments to check it:

- Before changing a number that looks arbitrary. It usually is not.
- Before proposing an approach that feels obvious. If it was obvious and it was not done,
  there is a reason, and it is probably written down.
- When onboarding into an area you have not touched.
- When something surprises you. Surprise is the signal that your model of the system is
  wrong, and the log is where the correction lives.

If you find an entry that contradicts what you were about to do, **say so before doing it**.
Maybe the decision expired and the log needs an update; maybe you were about to undo
something on purpose. Both are fine. Doing it silently is not.

## Keeping it honest

- **An entry that turned out wrong gets a correction, not a deletion.** Add a new entry on
  top explaining what changed and why the old reasoning stopped holding. The wrong reasoning
  is valuable: it stops the next person from arriving at it again.
- **Prune what stopped mattering.** A decision about code that no longer exists can go. The
  file describes the system as it is.
- **One paragraph beats five.** If you cannot say why in a paragraph, you probably have not
  finished deciding.
