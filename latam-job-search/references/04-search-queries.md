# Search strategy

## The two tools

Both live in `tools/`, run on `bun`, need no API key and no login.

```bash
# LinkedIn public job board, any country or "Remote"
bun run <skill-dir>/tools/linkedin-search/cli/src/cli.ts search \
  -q "<title>" -l "<Country>" --jobage 14 --limit 15 --format json

bun run <skill-dir>/tools/linkedin-search/cli/src/cli.ts detail <jobId> --format plain

# freehire.dev aggregator, region and skill facets
bun run <skill-dir>/tools/freehire-search/cli/src/cli.ts search \
  -q "<title>" --region latam --country AR --jobage 14 --limit 20 --format json

bun run <skill-dir>/tools/freehire-search/cli/src/cli.ts detail <slug> --format plain
```

Run the first search of a session with `bun --version` to confirm bun exists. If it does
not, fall back to `WebSearch` with the `site:` templates below and say so in the output.

Useful freehire facets: `--region latam|us|eu|global`, `--country AR,MX,CO`,
`--skill <canonical-skill>`, `--seniority`, `--company <slug>`, `--remote remote`.

## Query design

Four passes, in this order. Stop early once the target count is met with postings that
cleared the gates.

**Pass 1, titles.** Take the user's priority-ordered role families and run each as a
LinkedIn query scoped to their country, plus a freehire query scoped to their region.
Run several title variants per family: job titles are unstable, and the same role is
posted under three names in the same week.

**Pass 2, skills.** Query the freehire skill facets for the user's primary stack. This
finds postings whose title gave no signal but whose requirements are an exact match, and it
is consistently a better yield than generic English-language title searches.

**Pass 3, companies.** For every company on the user's watch list, run a company-slug
search. Any opening at a company the user already named as a reference point is worth
surfacing even when the specific role differs from what they asked for.

**Pass 4, widening, only if short.** Broaden the recency window from 14 to 21 or 30 days,
add adjacent titles, and add a region-agnostic remote sweep. Note in the output that the
window was widened, and for which passes.

## WebSearch fallback templates

For portals with no CLI, for a company's own careers page, or when bun is missing:

```
site:linkedin.com/jobs "<title>" remote
site:linkedin.com/jobs "<title>" <country> OR LatAm
site:<company>.com careers "<title>"
"<title>" "<country>" remote -site:linkedin.com
```

ATS boards answer directly and are worth hitting when a company is known:

```
https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true
https://boards-api.greenhouse.io/v1/boards/<org>/jobs/<id>
```

These return structured JSON including the full country list and, often, the compensation
band. They are the fastest way to resolve the "is my country actually eligible?" question
that Gate 2b asks, because JavaScript-rendered ATS pages return nothing useful to a plain
fetch.

## Recency

Default to 14 days. Include an older posting only when its deadline has not passed, and
label it with its date. When a date cannot be determined, include it flagged as
`date unknown` rather than silently.

## Volume discipline

- Cap each call at roughly 15 to 25 results.
- Run independent searches in parallel; do not serialize what does not depend on the
  previous answer.
- Fetch full details only for postings that survive the title and snippet pre-filter.
- Both portals rate-limit. A 429 is a back-off signal, never evidence that a portal is
  broken. Keep volume low: the LinkedIn CLI reads public pages, and automated access is
  against LinkedIn's terms of service, so this is a personal-use tool.

## Adapting to a focus argument

When the user passes a focus (`/job-search voice AI`, `/job-search fintech`), run the
matching role family first and generate two or three focus-specific query variants on top
of the standard passes, rather than replacing them.
