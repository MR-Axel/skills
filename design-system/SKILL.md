---
name: design-system
description: >
  Establish a design system where there is none, and enforce the one that exists so
  violations fail a check instead of surviving code review. Covers token layers, the traps
  that make tokens quietly wrong (alpha over variables, contrast by threshold, a token that
  cannot express a state), and the four gates that keep drift out. Use for: design system,
  design tokens, tokens, theme, dark mode, light mode, colores del sistema, hardcoded
  colors, /design-system, esto no respeta el design system, unificar estilos.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Design system

Two jobs, and which one you are doing depends on what already exists.

Read the design system section of `.claude/project-profile.md` first.

- **The profile records a design system** → your job is **enforcement**. Skip to the second
  half.
- **It does not** → your job is **establishing one**, then recording it in the profile so
  every other skill stops guessing.

A note on where the value is. Most design system advice is about authoring: pick a scale,
name your tokens, three layers. That part is a good afternoon of work and it is not what
fails. What fails is six months later, when a third of the codebase uses the tokens, a third
uses hardcoded values that happen to match, and a third uses hardcoded values that used to
match. Nobody violated the system on purpose. It just was never possible to violate it
**loudly**.

So: establish quickly, enforce seriously.

## Establishing

### Layers

```
primitive  ──▶  semantic  ──▶  component
--blue-600      --color-primary   --button-bg
```

Primitives are raw values with no opinion. Semantics say what a value is **for**. Component
tokens exist only when a component needs to diverge from the semantic layer, which is rarer
than it looks; reach for one when you catch yourself overriding a semantic token in one
place.

The layer that earns its keep is the middle one. `--color-primary` survives a rebrand;
`--blue-600` used directly in forty components does not.

### What a token has to be able to express

This is the trap that produces a system people abandon. **A token that cannot express a
state forces a hardcoded value at exactly the moment the design gets interesting.**

If your accent is `--color-primary`, then a tinted background at 12%, a border at 35% and a
hover at 90% are all things a real interface needs. Decide now how those get expressed. Two
ways work:

- Each variant is **its own token** (`--primary-soft`, `--primary-med`, `--primary-strong`).
  More tokens, no runtime math, works everywhere.
- The token is stored as **channels**, so alpha can be composed at use time
  (`rgb(var(--primary-rgb) / 0.12)`).

What does **not** work is a helper that takes a colour and an alpha and returns a colour,
applied to a CSS variable. At the moment it runs, the variable is the string
`var(--color-primary)`, not a colour. Depending on the helper, you get the opaque colour
back (so your subtle tint paints solid) or something the platform drops silently. Both
failures look like a styling mistake and are actually an architecture one, which is why they
survive so long.

### Contrast is computed, not eyeballed

Text on a coloured surface needs a real contrast decision. The naive version, "if the
background is light use dark text", is a luminance threshold, and it is wrong near the
middle of the range in exactly the cases you ship: mid saturation brand colours.

Compute the actual ratio against both candidates and take the better one. It is five lines,
it is deterministic, and it removes a whole category of "this looks fine on my monitor".

### Both themes or one, deliberately

If the product has light and dark, **every token is defined in both**. A token that only
exists in one theme is a page that half works, and it will be found by a user before it is
found by you.

If it commits to a single visual world, that is a legitimate choice. Write it down in the
profile so nobody adds a half finished second theme later thinking they are completing
something.

## Enforcing

The difference between a design system and a style guide is that one of them fails a check.

Four gates, in the order they pay off. Details and the subtleties that make each one
actually hold: [`references/enforcement.md`](references/enforcement.md).

1. **Ban the hardcoded value.** A test that greps the UI layer for raw colours and rejects
   them. The subtlety is that a naive grep is trivially defeated by an alias or a ternary,
   and a gate people route around is worse than none.
2. **Gate the generated artifact.** If tokens compile to CSS, a JSON theme or a native
   file, the committed output is regenerated in CI and compared byte for byte. Otherwise it
   drifts, and a drifted artifact is worse than no artifact: it looks authoritative.
3. **Assert contrast.** The ratio for every foreground and background pair the system can
   produce, as a test. Not a checklist item in a review.
4. **Assert theme completeness.** Every token defined in every theme. This is a set
   comparison, which means it is five lines and it never has an opinion.

None of these needs a visual regression tool. They are text assertions over your own source,
which is why they are worth writing before you reach for screenshots.

## Component patterns

When adding to an existing system, match the existing shape before inventing one. The
patterns worth writing down, and the anti patterns that produce most of the layout bugs, are
in [`references/patterns.md`](references/patterns.md).

The short version of the most common one: a flex item that grows without a bound will
happily eat the row when the container changes width, and the bug appears in a different
screen from the one you were building.

## Recording it

Once established, write it into `.claude/project-profile.md`: where the tokens live, which
file is the source of truth, the scales, the icon set, and **which file must never be edited
by hand** if something is generated.

That last one matters more than it sounds. A generated file that looks editable will be
edited, the change will vanish on the next build, and the person who made it will conclude
the design system is broken. They will be right.
