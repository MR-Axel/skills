# The four gates

A design system is a style guide until something fails when you violate it.

These are text assertions over your own source. No screenshots, no visual regression
service, no extra infrastructure. They run in the suite you already have.

---

## 1 · Ban the hardcoded value

A test that reads the UI source and rejects raw colours where a token exists.

The naive version is a grep for `#` and it does not survive contact with a real codebase.
Three things defeat it, and all three happen by accident rather than malice:

**Comments.** A hex in a comment explaining what a token equals is not a violation, and if
your gate flags it, the first thing someone does is stop trusting the gate. Strip comments
before matching.

**Aliases.** Someone writes `const c = COLOR.surface.raised` and then uses `c`. A gate that
only looks for the literal token path sees nothing. If your ban is on a *function applied to
a token*, resolve one level of aliasing, or check the call site by shape rather than by name.

**Ternaries.** `bg={dark ? '#12161F' : COLOR.surface.raised}` passes a gate looking for
assignment and fails the design system in exactly the case that matters. Match the value
wherever it appears, not where you expect it.

For colours specifically, the check that generalises best is **by luminance, not by string**.
A gate that bans "dark hardcoded surfaces" computes the luminance of every hex it finds and
rejects the ones below your threshold. That catches `#12161F`, `#131720` and the one someone
sampled from a screenshot, without maintaining a list.

Allow an escape hatch with a required reason, and make it noisy: an inline marker plus a
comment saying why. Real exceptions exist (a third party widget, a brand asset with a fixed
colour). What you are preventing is the silent exception.

---

## 2 · Gate the generated artifact

If tokens compile into anything, the committed output is regenerated in CI and compared to
what is in the repo, byte for byte. Any difference fails.

Without this, the generated file drifts from its source and becomes actively harmful: it
looks authoritative, it is committed, and it is wrong. Someone reads it, believes it, and
builds on a value that no longer exists anywhere else.

Two practical notes:

- **Line endings will bite you** on a mixed platform team. Normalise before comparing, or
  the gate goes red for everyone on the other operating system and gets disabled within a
  week.
- **The failure message should say the command**, not just "output differs". `run npm run
  gen:tokens` turns a confusing red into a five second fix.

---

## 3 · Assert contrast

For every foreground and background pair the system can produce, assert the ratio meets your
bar (4.5:1 for body text, 3:1 for large).

The value of doing this as a test rather than an audit is that it covers pairs nobody
designed. If a user picks their accent colour, or a subject gets a generated colour, the
combinations that reach production were never in a mockup. A test enumerates them; a review
cannot.

If you have a helper that picks a readable foreground, this is also where you catch it doing
the wrong thing, because the assertion is on the output rather than on the intent.

---

## 4 · Assert theme completeness

Every token defined in every theme.

A set comparison over the token definitions. Five lines, no judgement calls, and it catches
the specific failure where a page half works because someone added a token to dark and
forgot light. That one is invisible in development if you only ever look at one theme, which
is what everybody does.

Worth adding alongside: if your theme switching relies on a specific mechanism (a data
attribute on the root, a class, a media query), assert that the mechanism is intact. When
theme switching breaks, it usually breaks completely, and a one line test catches it before
a user does.

---

## What none of this covers

These gates protect **values**. They say nothing about whether the interface is any good.

Spacing that follows the scale can still be wrong. Type that uses the right token can still
be unreadable at the size you shipped. An interface can be perfectly token compliant and
still confusing.

That is what [`ux`](../../ux/) is for, and it is a different job done by a different pass.
Do not let a green gate stand in for having looked at the thing.
