---
name: deploy-qa
description: >
  Guided QA after a deploy. Reads the diff that shipped, maps changed paths to the areas
  they can break, decides the depth (smoke, selective regression, full regression) from
  blast radius instead of habit, and walks a concrete test list. Starts by proving the new
  build is actually live, because a deploy that reports success can still be serving the old
  bundle. Use for: que pruebo despues del deploy, deploy QA, smoke test, verificar deploy,
  post deploy check, /deploy-qa, se rompio algo con el push, que testeo de este cambio.
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Deploy QA

What to test after a push, decided from what actually changed.

Two failure modes this exists to prevent. One is testing nothing, because the change "was
small". The other is running the same forty step checklist for every change, which people
stop doing honestly by the third time, and a checklist that gets rubber stamped is worse
than none: it produces a record saying the thing was verified.

The depth comes from blast radius, not from habit.

Read `.claude/project-profile.md` for the deployed URL and the commands. This skill runs
**after** the release: [`deploy`](../deploy/) gets the build out, this one checks whether
it survived contact with production.

## Step 0 · Prove the new build is live

Before testing anything, confirm you are testing the new code.

This step exists because of how often it is the answer. A deploy reports success and serves
the previous bundle. A platform shows green while the container failed its health check and
rolled back. Someone spends forty minutes concluding the fix did not work, and the fix was
never there.

Check, in order:

1. **The platform says the new version is healthy.** Not "deploy finished". Healthy, and
   running the commit you expect.
2. **The served artifact changed.** Asset hash, build id, or a version endpoint. Compare
   against what was there before. This is the one that catches the lie.
3. **The logs are clean on boot.** Repeated 404s on your own API usually mean a handler that
   exists in the repo and was never registered in the production router.

If any of these is off, stop. There is nothing to QA yet.

Note: **if your platform does not report status back to your git host, a green checkmark on
the commit means nothing.** Check the platform.

## Step 1 · Read the diff

```bash
git log --oneline -1
git diff --name-only HEAD~1..HEAD
git diff --stat HEAD~1..HEAD
```

You are looking for two things: which areas the change can reach, and whether anything came
along that was not part of the intended change.

## Step 2 · Map paths to blast radius

Classify each changed path. The categories that matter are about **reach**, not about
folders:

| What changed | Reach | Depth |
|---|---|---|
| Root layout, app shell, global providers | every screen | full regression |
| Shared helper, util, hook used widely | every consumer, grep them | full regression |
| Design tokens, theme, global styles | every screen, visually | visual regression |
| Route registry, router config | every endpoint or page | full regression |
| Auth, session, permissions | every logged in path, and the logged out one | full regression |
| Payments, billing, anything with money | that flow, end to end, with real states | full regression of that flow |
| One feature area, self contained | that area | smoke |
| One new component, no shared edits | where it renders | smoke |
| Copy, comment, docs | nothing at runtime | eyeball it |

**Build your own version of this table for your repo, once.** The generic one gets you
started; the one that names your actual folders is the one people use.

Two rules that decide the ambiguous cases:

- **Shared code is not a small change.** A three line edit to a helper with forty callers is
  a forty caller change. Grep before deciding.
- **Sensitivity beats size.** Anything touching money, auth, or data deletion gets the deep
  pass regardless of how few lines moved. The cost of being wrong is not proportional to the
  diff.

## Step 3 · Write the list, then run it

Turn the blast radius into concrete checks. Each one names a route or a command, what to do,
and what should happen. "Check the dashboard" is not a check; "open the dashboard as a user
with no data, the empty state offers the primary action" is.

Always include:

- **The golden path of what changed.** The thing the feature is for, done the way a user
  does it.
- **One thing that already worked.** The cheapest regression signal there is.
- **The first thing that breaks if the change is wrong.** You usually know what this is; if
  you do not, that is a sign you do not understand the change well enough to QA it.

Run against **production**, not localhost. The point of post deploy QA is catching what only
breaks with real config: a missing env var, a build time variable that never got set, a
route that exists locally and not in the deployed router.

## Step 4 · Report

```markdown
## Deploy QA · <commit>

**Build live**: confirmed how
**Depth**: smoke / selective / full, and why

### Checked
- [pass] what, and what you saw
- [fail] what, and what happened instead

### Not checked
What you left out and why. Name it.

### Verdict
OK / OK with caveats / roll back
```

**Report what you did not check.** An area you skipped and named is a risk someone can
weigh. An area you skipped silently reads as verified, and that is how a QA report becomes a
false promise.

## When something is broken

Decide **roll back or fix forward** before starting to debug, and say which. The two have
different urgencies and it is easy to slide into a long debugging session while production
is broken, which is the worst of both.

Roll back when: users are hitting it now, or the cause is not obvious in the first few
minutes.

Fix forward when: the cause is known and the fix is small and safe.

Either way, the incident goes into the memory file afterwards (see
[`feature-agents`](../feature-agents/)), with the part that matters most: **which gate would have caught it**. That is the
line that turns an outage into a permanent improvement.
