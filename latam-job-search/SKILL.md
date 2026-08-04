---
name: latam-job-search
description: >
  Remote job search for LatAm-based candidates. Runs an onboarding interview to capture
  location, work modality, timezone tolerance, compensation floor, language levels and
  hard exclusions, then searches LinkedIn and freehire, verifies each posting against
  those gates before scoring it, and returns a deduplicated daily digest. Use for: buscar
  trabajo, búsqueda laboral, find jobs, job search, remote jobs, LatAm jobs, daily job
  digest, evaluate a job posting, is this job a fit, /job-search, /job-setup.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, Bash(bun --version), Bash(bun run *cli.ts *), Bash(curl -s https://api.ashbyhq.com/*), Bash(curl -s https://boards-api.greenhouse.io/*)
---

# LatAm job search

A job search that filters on the things that actually disqualify a remote LatAm candidate,
before it spends any effort on fit: **work modality, country eligibility, timezone overlap,
compensation floor, and language level.**

Most job tooling scores first and checks eligibility later, which is how a LatAm candidate
ends up reading a beautifully matched posting that turns out to be hybrid in another city,
locked to a single foreign country, quoted in a currency they will not accept, or built
around daily calls in a language they read better than they speak. This skill inverts that
order. Gates first, scoring second, and every gate comes from an answer the user gave at
setup, not from a guess.

## Commands

| Command | Does |
|---------|------|
| `/job-setup` | Onboarding interview, writes `job-search/profile.md`. Run once. |
| `/job-search` | One search run: search, gate, score, dedupe, present. Accepts an optional focus, e.g. `/job-search voice AI`. |
| `/job-evaluate <n>` | Full fit evaluation of posting `n` from the last digest. |
| `/job-track` | Record an application in `job-search/tracker.csv`. |

Plain language works too: "buscá trabajo", "any new jobs today?", "¿esta oferta me sirve?".

## Workflow

### First run

If `job-search/profile.md` does not exist, run the interview in
`references/01-onboarding.md` and stop. Do not search in the same turn: the user just
answered fifteen questions and a wall of results is not a reward.

Create the state files from `assets/` on first search, not at setup:
`job-search/seen_jobs.json` and `job-search/tracker.csv`.

### Every run

1. **Load state.** Profile, seen jobs, tracker. A run has no memory of previous
   conversations, so read the files rather than assuming.
2. **Search.** Four passes from `references/04-search-queries.md`: titles, skills,
   watch-list companies, then widening only if short.
3. **Gate.** Apply `references/02-eligibility-and-location.md` in order. Cheap gates
   (modality, dedupe) run before expensive ones (fetching the full posting). Keep a tally
   of what each gate removed.
4. **Score.** Quick high / medium / low for the digest. Full framework
   (`references/03-fit-evaluation.md`) only when the user asks about a specific posting.
5. **Persist.** Write every posting seen, presented and rejected, to `seen_jobs.json`.
6. **Present.** One table, one highlight, the filter tally. Format in
   `references/05-daily-run.md`.

## The rules that matter

These are the ones that cost real time when they were missing:

1. **Never score a posting on its title or its aggregator tag.** Fetch the description.
   `work_mode: remote` frequently means "some remote is possible", not "your country is
   eligible".
2. **Modality is a hard filter, not a preference.** If the user said fully remote, hybrid
   postings do not appear, including hybrid in the user's own city. Report the count
   dropped so the filter stays visible and correctable.
3. **"Remote, globally" is a claim to verify.** Find the actual country list, usually in
   the application form or the ATS API. A posting that says "we hire wherever talent is"
   and accepts three named countries is common.
4. **A single-country remote tag is a fail** unless that country is the user's, or the
   posting is explicitly multi-country, region-wide, or anywhere.
5. **Check compensation the moment a number appears,** against the floor and against what
   that class of employer can structurally pay. Put the mismatch in the row, not a footnote.
6. **Weight a language requirement by what the job does all day,** not by the requirements
   list. Fluent English on a spec-writing role is a small risk; on a role that is eight
   client calls a day it is the whole job.
7. **The same title is two different jobs.** Read the qualifications every time and say in
   the output which kind it turned out to be.
8. **Dedupe by company plus role, not URL.** The same posting is mirrored across LinkedIn,
   the company ATS and two aggregators, with a different URL and often a different title.
9. **Classify the employer on three axes, not one:** relationship (direct, consultancy,
   staffing intermediary, aggregator repost), type and stage (early startup, scale-up,
   enterprise, PE-owned, bootstrapped, public sector), and sector. A user can want a
   startup and refuse consultancies, or want fintech and refuse gambling, and none of that
   is inferable from the role title. A refused sector is a hard drop; a deprioritized
   employer class is labeled, never disguised.
10. **Verify the link resolves to the actual posting.** Aggregator URLs rot and ATS
    shortcodes get retired, and the board then serves a generic page with HTTP 200, so a
    status check passes while the link is dead. Prefer the canonical ATS source or API,
    confirm the posting's own title is in what you fetched, and if you cannot confirm it,
    link the employer's job board and say so.
11. **Never fabricate a posting, a contact, or a company fact.** Everything presented comes
    from real CLI or fetch output. Referral help is a LinkedIn search link the user opens
    themselves, never a scraped person.
12. **Never pad a thin day.** Say the pool was thin and why. A list padded past the user's
    own hard gates teaches them to stop reading it.
13. **Honesty constraints carry into anything written afterwards.** Nothing from the
    never-claim list, and an in-progress credential is never marked complete, including
    when the user suggests it.

## Files

```
latam-job-search/
├── SKILL.md
├── references/
│   ├── 01-onboarding.md              the interview, run once
│   ├── 02-eligibility-and-location.md the gates, applied every run
│   ├── 03-fit-evaluation.md          scoring, for postings that cleared the gates
│   ├── 04-search-queries.md          the tools and the four search passes
│   └── 05-daily-run.md               the run loop and the output format
├── assets/
│   ├── candidate-profile.template.md
│   ├── seen_jobs.template.json
│   └── tracker.template.csv
└── tools/
    ├── linkedin-search/              bun CLI, public job board, no auth
    │   ├── USAGE.md                  flags and examples, read before invoking
    │   └── cli/
    └── freehire-search/              bun CLI, aggregator with region and skill facets
        ├── USAGE.md
        └── cli/
```

Read a tool's `USAGE.md` before calling it. Do not guess flags: both CLIs validate them
and exit non-zero on an unknown one.

## Requirements

- [bun](https://bun.sh) for the two portal CLIs. Without it the skill falls back to
  `WebSearch` and says so in the output.
- No API keys, no logins, no accounts.

## Privacy

Everything the skill learns lives in `job-search/` in the user's own workspace and is
never transmitted anywhere. Add `job-search/` to `.gitignore` if the workspace is a
repository: the profile holds compensation numbers and the tracker holds an application
history.

The LinkedIn CLI reads public job pages. Automated access is against LinkedIn's terms of
service, so keep volume low and treat this as a personal-use tool.
