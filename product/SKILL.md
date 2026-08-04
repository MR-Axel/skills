---
name: product
description: >
  Review a change from the product and business side: does it serve the user need, are
  the tier gates right, are the states complete, is it discoverable. Reads your product
  model from .claude/project-profile.md. Use before shipping. Use for: product review,
  does this make sense, /product.
license: MIT
allowed-tools: Read, Grep, Glob, Bash(git diff *)
disable-model-invocation: true
---

# Product review

Review $ARGUMENTS, or the working diff, as the person accountable for whether this feature
is worth shipping.

Read the **product context** section of `.claude/project-profile.md`: who the users are,
how the product makes money, what the tiers are, which actions matter. If that section is
empty, say so and review only user flow completeness and discoverability. Do not invent a
business model, and above all do not import one from another product: gating advice built
on a pricing model this project does not have is worse than no advice.

## 1. Does it serve the need

Start here, because it is the question most product reviews skip in favour of checklists.

- What user problem does this solve, and does the implementation actually solve it or just
  gesture at it?
- Is there a materially simpler version that gets most of the value?
- Does it fit how the rest of the product works, or does it introduce a second way to do
  something that already exists?
- What does it cost: added surface to maintain, a new concept for users to learn?

If the honest answer is that the feature does not serve the stated need, say that. It is
the single most valuable thing this review can produce, and the most likely to be omitted.

## 2. Tier gating

Only if the project has tiers.

- Is the new capability on the correct side of the line, per the profile's model?
- Can a user on a lower tier reach the data anyway through the API or the network tab?
  A gate enforced only in the UI is not a gate.
- Does the lower tier remain genuinely useful? Over-gating produces churn, not upgrades.
- When someone hits the gate, do they understand what they would get and how to get it,
  in one step?
- Are the tier comparison and billing surfaces updated to match what shipped?

## 3. Flow completeness

- Happy path works end to end, including the second time (idempotency, duplicate submits).
- Loading, empty, error and success states all exist and say something useful.
- Reversibility: can the user undo, edit or delete what they just created?
- Permissions: what does this look like logged out, or for a user who lacks access?

## 4. Discoverability

A feature nobody finds was not shipped. Is there a path to it from where a user would
look? Do existing users find out it exists?

## 5. Data and messaging

- New fields have sensible defaults for rows that already exist.
- Access rules cover the new data. Deleting a user removes what should be removed.
- Anything that sends a message to a user: is there a preference for it, an unsubscribe
  where required, and a frequency that will not become a reason to mute the product?
- Is the action this feature is supposed to move actually measurable? If the profile lists
  the metrics this project tracks and none of them would move visibly, say so.

## Output

```
Product context: <from profile | none recorded, sections skipped>

NEED:            ok | concern, <one line>
GATING:          ok | concern | n/a, <one line>
FLOW:            ok | gaps, <one line>
DISCOVERABILITY: ok | concern, <one line>
DATA:            ok | gaps | n/a, <one line>
MESSAGING:       ok | gaps | n/a, <one line>

VERDICT: SHIP | SHIP WITH FOLLOW-UPS | NEEDS CHANGES
```

`NEEDS CHANGES` requires a concrete blocker: a broken flow, a real data exposure, a gate
that does not hold. Do not block a change over a difference of product opinion. State the
disagreement, recommend, and let the person shipping decide.
