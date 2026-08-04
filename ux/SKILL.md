---
name: ux
description: >
  Audit UI for responsiveness, accessibility, design system consistency and interaction
  states, against the design system in .claude/project-profile.md. Use for: UX review,
  audit this component, accessibility check, /ux.
license: MIT
allowed-tools: Read, Grep, Glob, Bash(git diff *)
disable-model-invocation: true
---

# UX audit

Audit $ARGUMENTS, or the components touched by the working diff.

Read the design system section of `.claude/project-profile.md` first. If the project has
no design system recorded, **say so at the top of the report**, point at
[`design-system`](../design-system/) for establishing one, and audit only
responsiveness, accessibility and interaction states. Consistency findings need a stated
standard to be consistent with; without one they are your taste, and you should not
report your taste as a finding.

## 1. Accessibility

The highest-value section, because these are real defects for real users and they are
almost always cheap to fix. Target WCAG 2.1 AA unless the profile says otherwise.

- Every interactive element has an accessible name: visible text, `aria-label`, or a
  labelled icon. An icon-only button with no label is invisible to a screen reader.
- Form inputs are associated with labels, not merely placed near text that looks like one.
- Placeholder text is not doing a label's job.
- Focus is visible on every interactive element, and focus order follows reading order.
- Everything reachable by mouse is reachable by keyboard. Custom dropdowns, modals and
  menus are where this breaks: check escape-to-close and focus trapping.
- Images have `alt`, and decorative images have empty `alt`, not a filename.
- Color is never the only carrier of meaning.
- Text contrast meets 4.5:1 (3:1 for large text). Check the actual token values from the
  profile rather than eyeballing it.
- Motion respects `prefers-reduced-motion` where anything animates.
- Live regions announce async results that appear without a page change.

## 2. Responsiveness

- Layouts reflow rather than overflow: check the narrowest supported width.
- Touch targets are at least 44x44 CSS pixels on touch viewports.
- Long or user-generated strings truncate or wrap instead of breaking the layout. Test
  mentally with a 60-character unbroken word and an empty string.
- Content hidden at a breakpoint is genuinely redundant, not the only path to an action.
- Tables and wide content scroll inside their own container; the page body never scrolls
  horizontally.

## 3. Interaction states

Every async or conditional surface needs all four, and the missing one is usually error:

- **Loading**, with the pattern the profile names.
- **Empty**, saying what would go here and offering the action that fills it.
- **Error**, saying what failed and what to do, never a bare "Something went wrong".
- **Success**, visible feedback that the thing happened.

Also: are controls disabled while an operation is in flight, so a double click cannot
submit twice?

## 4. Design system consistency

Only with a profile design system. Check the tokens, spacing, radius, typography scale,
icon sizing and section header patterns it defines, and flag values that were hand-written
where a token exists.

## Output

```
Design system: <from profile | none recorded, consistency checks skipped>

[SEVERITY] path/to/Component.ext:LINE, one-line claim
  Impact: <who is affected and how>
  Fix: <specific change>
```

`CRITICAL` unusable for some users (keyboard trap, unlabelled primary action, broken
layout at a supported width). `HIGH` significant friction. `MEDIUM` inconsistency.
`LOW` polish.

```
N issues (N critical, N high, N medium, N low)
Skipped: <sections not run, and why>
```

Do not manufacture findings to fill a section. "Nothing found" is a real result, and
saying it is what makes the other findings credible.
