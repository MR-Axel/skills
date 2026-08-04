# Patterns and anti patterns

Component patterns worth writing into a system, and the mistakes that produce most of the
layout and form bugs.

Every one of these is here because it was found in production, not because it is
theoretically nice.

---

## Layout

### The unbounded flex item

A card in a wrapping grid with `flex-grow` and no `max-width` looks perfect while you build
it and eats the entire row somewhere else. Usually in a view with a different container
width, which is why it gets found by someone other than the author.

```
flex-basis: 120px;   /* the size it wants */
flex-grow: 1;        /* allowed to fill */
min-width: 108px;
max-width: 180px;    /* the one that is always missing */
```

For a variant that should never stretch (an "add" tile, a secondary action), `flex-grow: 0`
instead of trusting the max.

### The flex child that will not truncate

A long unbroken string (a filename, an id, a URL) inside a flex row does not shrink to fit,
even with `flex-shrink: 1` and a one line clamp. Its minimum content width is the whole
string, so it overflows and crushes its sibling.

The fix is `min-width: 0` on the shrinking child. It is unintuitive enough that it gets
rediscovered every few months, which is why it belongs in the system rather than in
somebody's memory.

---

## Forms

### Errors: banner, inline, and progressive clearing

The pattern that fails: one `error` string rendered under the form. It scrolls out of view,
it does not say which field is wrong, and a form with four problems takes four submits to
discover them all.

The pattern that works has three parts together:

1. **Validate everything at once** and return all errors, not the first.
2. **A banner at the top** listing which sections failed, so the state is visible without
   scrolling.
3. **Inline markers** on each failing field or section.
4. **Progressive clearing**: touching a field clears its own error immediately.

That fourth part is what makes it feel responsive instead of accusatory. Without it the
user fixes a field, the error stays, and they cannot tell whether they fixed it.

Errors of validation are **not** toasts. A toast disappears, and the information the user
needs to act is gone with it. Toasts confirm that something succeeded.

### The double submit lock

`disabled={loading}` does not prevent a double submit. Between the first click and the
second, the state update has not rendered, so the second click hits an enabled button.

A synchronous ref, checked and set before any await, is what actually blocks it:

```
if (submitLock.current) return;
submitLock.current = true;
try { /* ... */ } finally { submitLock.current = false; }
```

This matters most on anything that creates a resource. Two POSTs from one impatient double
click create two records, or worse, the second arrives through a cache with an empty body
and fails in a way that looks like a server bug.

---

## Iconography

If the system bans emoji in the interface, ban them **in the interface** and be explicit
about where they are still fine. A blanket rule gets violated because the exceptions are
obviously reasonable, and once one rule is routinely ignored the others weaken too.

A version that survives contact with reality:

- **Banned**: chips, badges, buttons, headers, tabs, cards. Anywhere the emoji is standing
  in for an icon. Use the icon set, at the token colour.
- **Fine**: the voice of a character in a chat, transactional email, internal alerts,
  anything outside the product surface.

The distinction is whether the emoji is **carrying meaning in the UI** or **carrying tone in
a message**. The first is an icon in disguise and renders differently on every platform; the
second is writing.

---

## Spacing and type

Two rules that do more than a long scale:

**Pick a scale and stay on it.** The value of a scale is not that 8 is better than 7; it is
that the whole interface agrees. One off value is invisible; forty are why a product looks
unfinished without anyone being able to point at why.

**Give it more room than feels necessary.** The most common gap between a competent
interface and a good one is breathing room, and it is the cheapest thing to fix. If a form
feels tight, it is.

For type, define the scale by **role** rather than by size: eyebrow, body, body strong,
section title, card title, hero. A role survives a redesign, a size does not, and a
contributor picking a role makes fewer wrong choices than one picking a number.
