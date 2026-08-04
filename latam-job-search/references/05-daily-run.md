# Daily run playbook

The shape of one search run, whether triggered by hand or by a scheduled task. Optimized
for a person who reads it once with coffee and wants a table, not an essay.

## Step 0: load state

Read all four before touching a search:

| File | Why |
|------|-----|
| `job-search/profile.md` | Every gate threshold and preference comes from here |
| `job-search/seen_jobs.json` | Postings already surfaced, never show them twice |
| `job-search/tracker.csv` | Postings already applied to, dedupe by company plus role |
| `references/02-eligibility-and-location.md` | The gates, applied verbatim |

If the profile is missing, run the onboarding interview instead and stop.

A scheduled run has no memory of previous conversations. Treat every run as a cold start
and actually read the files: do not assume yesterday's context carries over.

## Step 1: search

Run the four passes from `04-search-queries.md`. Collect every result into one pool,
tagged with the portal it came from.

## Step 2: gate

Apply `02-eligibility-and-location.md` in order, cheapest first. Modality and dedupe are
cheap and remove the most; fetch the full posting only for what survives them.

Keep a **drop tally by gate**. It costs nothing and it is the only way the user can tell a
thin day from an over-aggressive filter.

## Step 3: score

Quick fit only (high / medium / low) for the digest. Reserve the full framework in
`03-fit-evaluation.md` for postings the user asks about by number.

## Step 4: persist

Append every posting seen this run, presented **and** rejected, to `seen_jobs.json`:

```json
{
  "seen": {
    "<normalized-url>": {
      "title": "...",
      "company": "...",
      "url": "...",
      "first_seen": "YYYY-MM-DD",
      "fit": "high|medium|low",
      "status": "new|skipped",
      "portal": "linkedin-search|freehire-search",
      "dropped_by": "modality|location|comp|language|dedupe|null"
    }
  }
}
```

Writing the rejects is what stops the same dead posting from being re-evaluated every
morning, and `dropped_by` is what lets the user audit the filter later.

Use the real current date for `first_seen`. Never guess it.

## Step 5: present

One table, sorted by fit, then a short highlight. That is the whole report.

```
# Job search, YYYY-MM-DD

| # | Fit | Role | Company | Link | Pros | Cons |
|---|-----|------|---------|------|------|------|

**Best match: <role> at <company>.** Two or three sentences on why, and the one
thing to check before applying.

Near-misses (not listed): <company> <role>, <reason it failed the gate>.

Filtered: N hybrid, N wrong country, N below comp floor, N refused sector, N already seen.
Coverage: N searches across <portals>. N new postings written to seen_jobs.json.
```

Rules for the table:

- **Pros and cons must be specific to the posting.** "Explicit Argentina eligibility,
  n8n and Claude API named in the stack" is useful. "Good match, competitive company" is
  filler and trains the user to skip the column.
- **Put the disqualifying fact in the cons cell, not in a footnote.** A published band
  below the walk-away line, a required degree the user does not have, a 15-year experience
  bar: these belong in the row where the user reads them.
- **Say which kind of role an ambiguous title turned out to be** (Gate 6). "FDE, and it is
  the backend-engineering kind" saves a click.
- **Label the employer** when it is not a direct hire, and name the type and sector when
  either is something the profile cares about: "staffing intermediary, client undisclosed",
  "Series B fintech", "enterprise, PE-owned". One short parenthetical, not a paragraph.
- **Link the canonical posting**, and if the only reachable link is an aggregator mirror,
  say so in the row so the user knows before clicking.

## Step 6: thin days

If the run cannot reach the target count with postings that cleared every gate, present
what there is and say plainly how many searches ran and why the pool was thin.

**Do not pad the table with postings that fail the user's hard gates.** A list padded to a
round number teaches the user that the filter does not mean anything, and the next real
match gets skimmed past with the filler.

## Step 7: offer the next step, once

End with a single line offering a deeper evaluation by number. Do not run it unprompted,
and do not append a second table of "bonus" results.
