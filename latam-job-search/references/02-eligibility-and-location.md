# Eligibility, location and comp gates

These are pass/fail gates, not scoring dimensions. Run them **before** scoring a posting
and before spending a detail fetch on it. Every rule here exists because a real search
wasted real effort on a posting that looked fine until someone read the fine print.

The gates assume a LatAm-based candidate applying to remote roles, but nothing here is
Argentina-specific: substitute the user's own country, city, timezone and currency from
`job-search/profile.md`.

---

## Gate 0: read the posting before you score it

Never score a job on its title, its aggregator tags, or a search-result snippet. Fetch the
full description first (each portal CLI has a `detail` command; otherwise `WebFetch` the
URL).

Aggregators mislabel constantly. A `work_mode: remote` facet frequently means "this role
can involve some remote work", not "open to your country". A posting whose location field
lists two cities is hybrid in those cities regardless of what the tag says.

**Budget rule:** pre-filter on title and snippet, then fetch details only for postings that
survive the pre-filter. A run that fetches everything is slow and adds nothing.

---

## Gate 1: work authorization

Read the eligibility, work rights, or "who can apply" section verbatim and classify:

| Posting wording | Verdict |
|-----------------|---------|
| Names a citizenship or permanent-residency requirement | **FAIL, hard stop.** Quote the exact wording back to the user. |
| Requires a security clearance at any level | **FAIL** in most countries, since clearance is normally gated on citizenship. |
| Explicitly names the user's status, or says "we sponsor" / "international applicants welcome" | **PASS**, verified. Worth citing as a positive in the application. |
| Silent on citizenship or residency | **PROCEED, marked unverified.** Check the employer's careers page before drafting anything. |

Two failure modes worth naming:

- **Silence is not permission.** Large programs routinely gate eligibility on their own
  website rather than in the ad. Highest risk: professional services, government and
  defence, banking, telecoms, critical infrastructure.
- **A company-wide "we hire globally" statement is not role-level permission.** The common
  pattern is a warm general welcome followed by a named list of the countries or business
  units it actually covers. Confirm the specific posting appears on that list.

Report an eligibility failure **with the quoted source**, never as a silent drop. The user
may know something about their own status that the profile does not record.

---

## Gate 2: work modality

**Run this before anything else in the location family, and treat it as a hard filter, not
a preference.** The user answered a modality question at setup. That answer is binding: if
they said fully remote, a hybrid posting does not appear in the results table at all, not
ranked low, not labeled, not "worth a look because the rest is great". It is dropped.

| Profile answer | Fully remote posting | Hybrid in user's city | Hybrid in another city | Onsite | Modality not stated |
|----------------|:--------------------:|:---------------------:|:----------------------:|:------:|:-------------------:|
| Fully remote only | PASS | **FAIL** | FAIL | FAIL | Verify; drop if it cannot be confirmed remote |
| Remote, hybrid OK in my city | PASS | PASS | FAIL | FAIL | Verify |
| Hybrid or onsite in my city | PASS | PASS | FAIL | PASS if in city | Verify |
| Open to relocation | PASS | PASS | PASS | PASS | Verify |

Four things that make this gate work:

1. **Read modality from the posting body, not the title or the tag.** "Hybrid" hides inside
   benefits sections ("hybrid scheme at our offices in ..."), inside a location line, or in
   an office-days sentence halfway down. A posting tagged remote that says "2 to 3 days per
   week in office" is hybrid.
2. **Hybrid in the user's own city is still a fail when they said fully remote.** This is
   the exact mistake this rule exists to prevent. Being able to reach the office does not
   make the role remote, and a user who asked for remote is telling you about how they want
   to work, not about geography.
3. **Silence is not remote.** A posting that names an office location and never says remote
   is unverified. Confirm it, or leave it out. Never upgrade "based in X" to "remote from X".
4. **Report what the gate removed.** End the run with a line like
   `dropped by modality gate: 6 hybrid, 2 onsite`. Silent filtering looks identical to a
   thin day, and the user cannot tell you the filter is wrong if they cannot see it working.

Hybrid postings that fail this gate may be mentioned **once**, in a single closing line
outside the results table, only if the user's thin-day preference allows near-misses and
only labeled as modality failures. They never occupy a numbered row.

---

## Gate 2b: location

### Marketing copy is not an eligibility list

"This role is remote, so it can be executed globally" and "we prioritize your talent, not
your location" are **claims to verify**, not facts. A real posting carrying exactly that
language turned out to accept three named countries, and the list was visible only in the
application form's country dropdown, not anywhere in the prose.

When a posting looks great on remote-and-global language alone, go find the actual list:
the application form, the careers-page detail, the ATS job-board API. Until you find it,
the posting is **unconfirmed**, not high-fit.

### A single-country remote tag is not enough

A posting that is remote-within-Colombia-only, remote-within-Mexico-only, or
remote-within-Brazil-only means the user is not eligible unless that country is theirs.
Being in the same region does not help.

The bar is one of:

- the posting explicitly includes the user's country, or
- it is explicitly open across multiple countries, region-wide, or "anywhere".

A single foreign country name in the location field, even tagged remote, defaults to
**FAIL** until the body text says otherwise.

### Hybrid geography, when the profile allows hybrid at all

Only reachable if Gate 2 admitted hybrid at all. Then this is arithmetic, not preference:
a person can be physically present in one city, so a hybrid role anchored to any other city
is exactly as disqualifying as a fully onsite role there, however good the rest of the fit
looks. Check the office city explicitly, because "hybrid" in a title often hides it.

### A lone city name with no remote language is uncertain, not remote

A posting listing only "New York" or "São Paulo" with no explicit remote or work-from-
anywhere statement is **onsite or uncertain**. Flag it as needing verification. Do not
present it as remote-friendly.

---

## Gate 3: timezone

Compute the offset against the user's own UTC offset and compare it to the tolerance in
their profile. Flag rather than silently pass when:

- The posting says "Remote, Europe" or is Europe-only, and the user is in the Americas
  (CET is 4 to 6 hours ahead of most LatAm offsets).
- Salary is quoted in a European currency as a local B2B contract, which usually implies
  local business hours.
- The posting targets a CIS or APAC market, where the gap is larger still.
- The posting names required overlap hours ("4 hours overlap with US Eastern",
  "core hours 9 to 5 CET"). Translate those into the user's local clock and show the result,
  because "9 to 5 CET" reads harmless until you write it as "4am to 12pm" for the reader.

An all-Americas or explicitly region-inclusive posting gets a small positive weight over an
otherwise equivalent Europe-only or APAC-only one. Overlap is real daily friction, not a
technicality.

---

## Gate 4: compensation

**Check the number the moment it appears.** Do not bury a comp mismatch in a footnote: a
posting whose published range sits under the user's walk-away line is a real mismatch even
when everything else fits.

Three checks:

1. **Against the floor.** Compare to the user's floor and walk-away numbers from the
   profile, normalising monthly vs annual first.
2. **Currency.** A number with no currency next to a location in a local-currency market
   should be treated as local currency until proven otherwise. When the user's profile says
   hard currency only, an employer that is domestically funded in a soft-currency market is
   **unlikely** to clear the floor: flag it as a probable comp mismatch, not a neutral
   unknown.
3. **Against the class of employer.** Match the ask to what that class can actually pay
   (see the onboarding round 2 table). A posting scoped "2 to 4 years" or "early career", a
   staffing intermediary, or a local-band employer structurally cannot support a senior
   hard-currency anchor. That is a property of the posting to flag, not a reason to lower
   the user's target everywhere else.

---

## Gate 5: language

Compare the posting's stated requirement against the per-language levels in the profile,
and weight it by **what the job actually does all day**. Like modality, this is driven by a
binding answer the user already gave (onboarding round 3), not by your judgement:

| Profile answer | Level demanded is at or below the user's | Level above the user's, async or written-heavy role | Level above the user's, live-facing role |
|----------------|:---:|:---:|:---:|
| Filter these out | PASS | Flag | **FAIL, drop** |
| Flag them, I will decide | PASS | Flag | Flag prominently in the row |
| No problem | PASS | PASS | PASS, note it |

"Live-facing" means the "what you'll do" section is dominated by customer calls, discovery
or onboarding sessions, QBRs, live enablement, executive presentations, or a sales quota.
Read that section, not the requirements list: a job can demand fluent English and still be
90% written specs, and a job can say nothing about language and still be eight calls a day.

- A posting demanding "advanced" or "fluent" English for a role dominated by live customer
  calls, discovery sessions, QBRs or executive presentations is a genuine risk for a B2
  speaker, not a checkbox. Honor the user's round-3 answer: drop it, or flag it loudly.
- The same requirement on a spec-heavy, async, internal-facing role is a much smaller risk.
  Read the "what you'll do" section, not just the requirements list.
- "English lessons offered" as a benefit does not rescue a role whose day-to-day **is**
  speaking that language to enterprise customers.
- A posting that states a level matching the user's exactly ("Upper-Intermediate or above"
  for a B2 speaker) is a positive signal worth calling out.

---

## Gate 6: role depth, or why titles lie

**The same title is routinely two different jobs.** "Forward Deployed Engineer" is the
canonical example and it has meant both of these in the same week:

- an AI-assisted builder role whose posting said outright "you do not need an engineer to
  ship your work", which is a genuine fit for a no-code or AI-tooling profile; and
- a role requiring "5+ years software or solutions engineering, backend service development
  in TypeScript, Python, Go" plus fluent professional English, which is a senior backend
  engineering job wearing a fashionable hat.

The second one scored "high fit" on title and location alone and only collapsed once
someone read the qualifications. So: **read the required-qualifications list every time,
and say in the output which kind of role it is.** The same warning applies to "AI Engineer",
"Solutions Architect", "Product Owner" and "Automation Specialist".

Also check the years-of-experience bar against the user's real numbers. A req asking 15+
years is not a stretch goal, it is a different job.

---

## Gate 7: who is actually hiring

Three separate questions, all answerable from the posting plus a quick look at the
company. Record all three, because a user can be fine with a startup and allergic to a
consultancy, or want fintech and refuse gambling, and none of that is inferable from
the role title.

### 7a. Employer relationship

- **Direct employer**, the company you would work for.
- **Consultancy or staff augmentation**, where the day-to-day work is a client's, not
  theirs, and the client may change.
- **Staffing or recruiting intermediary**, "one of our clients is hiring", employer
  undisclosed, and the agency takes a cut of the band.
- **Aggregator repost**, where this posting is a mirror and the real source is elsewhere.
  Find the original before presenting it: the mirror's URL is the one most likely to rot.

### 7b. Company type and stage

| Type | Read it from |
|------|--------------|
| Early-stage startup (pre-seed to Series A) | Small headcount, founder in the interview loop, equity emphasized over base |
| Scale-up (Series B and beyond) | Named funding rounds, hiring across several functions at once |
| Enterprise or large corporate | Multi-thousand headcount, req codes in the title, structured levels, formal process |
| PE or VC-owned portfolio company | Ownership named in the boilerplate, cost discipline, often a legacy product |
| Consultancy or agency | Sells its people's time, described by client logos rather than a product |
| Public sector, NGO, academic | Different pay bands and hiring rules entirely |
| Bootstrapped or small business | No funding mentioned, lean team, often the most autonomy |

Stage is not a proxy for quality, it is a proxy for **what the job feels like**: an
enterprise req is more process and narrower scope, an early startup is more ambiguity and
more surface area. Match against what the user said they want, not against prestige.

### 7c. Industry and sector

Record the sector, and check it against both lists in the profile: sectors the user wants
and sectors they refuse. Refusals are common and legitimate (gambling, defence, adtech,
crypto, tobacco, extractives, MLM, payday lending) and a user who named one should never
have to see it again. Treat a refused sector as a hard drop, not a low score.

Also note when a sector is a **positive** match to something the profile lists as domain
experience: regulated industries, logistics, health, fintech. That is worth surfacing in
the row, because it is often the difference between a generic application and a strong one.

### Applying the profile

For each of 7a, 7b and 7c, the profile says `exclude`, `label`, or nothing.

- `exclude`: the posting does not appear.
- `label`: it appears with the classification stated in the row, never disguised.
- nothing: it appears normally.

Labeling is the better default for employer relationship, because a staffing role can be
worth seeing as long as the user knows what it is before they click. Excluding is the
better default for refused sectors, because that answer will not change tomorrow.

---

## Gate 8: culture red flags

Grep the posting's own words for the phrases in the user's profile. If a description frames
internal confrontation as a virtue, demands constant availability, or matches any phrase
the user listed, **flag it prominently**, regardless of how good the pay or skills match
looks. A deal-breaker does not stop being one because the rest of the posting is attractive.

---

## Gate 9: deduplication

Dedupe by **company plus role**, not by URL. The same posting is routinely mirrored across
LinkedIn, the company's own ATS board, and two aggregators, with a different URL and often
a slightly different title on each.

Practical rules:

- Normalise before comparing: strip query strings, trailing slashes, and tracking
  parameters; lowercase; drop bracketed suffixes like "(Remote)" or "(LATAM)" from titles.
- Normalise the company too. "Kraken" and "Payward, Inc." are the same employer;
  "Dialpad" and "Dialpad Japan" are the same posting.
- Check both the seen-jobs state file and the application tracker.
- When the URL check passes but something feels familiar, do a company-plus-title pass by
  hand before presenting. A URL-only dedupe has repeatedly re-surfaced roles the user
  already applied to.

---

## Gate 10: the link has to work

Aggregator URLs rot. ATS shortcodes get recycled or retired when a req closes, and the
board then serves a generic "current openings" page **with HTTP 200**, so a status-code
check passes while the link is useless to the reader.

Before putting a URL in the results table:

- Prefer the **canonical source** over the aggregator mirror: the company's own ATS board,
  or the ATS API (`api.ashbyhq.com/posting-api/job-board/<org>`,
  `boards-api.greenhouse.io/v1/boards/<org>/jobs/<id>`). These return structured JSON that
  either contains the job or does not, with no SPA shell in between.
- **A 200 is not proof the posting exists.** Workable, Ashby, Greenhouse and Lever all
  render client-side, so a plain fetch returns the shell for a dead ID exactly as it does
  for a live one. Confirm the posting's own title appears in the payload you fetched.
- If a link cannot be confirmed, either present the **employer's job board** instead, with
  the role name to search for, or say the link could not be verified. Do not ship a URL
  you have not seen resolve to the actual posting.
- When a posting is only reachable through an aggregator, say so in the row. The user
  should know before they click that they may land on a mirror or a dead page.

---

## Quick reference

| Gate | Fails when | Output when it fails |
|------|-----------|----------------------|
| 0 Read first | Scored on title or tag alone | n/a, this is a process rule |
| 1 Authorization | Citizenship, PR or clearance required | Hard stop, quote the wording |
| 2 Modality | Hybrid or onsite when the profile says remote only | Drop from the table, report the count |
| 2b Location | Single foreign country, hybrid elsewhere, city-only | Drop, or flag as unverified |
| 3 Timezone | Overlap exceeds the profile tolerance | Flag with hours in local time |
| 4 Comp | Below walk-away, or wrong currency | Flag in the row, never a footnote |
| 5 Language | Level demanded above the user's, live-facing role | Drop or flag per profile |
| 6 Role depth | Qualifications do not match the title | Say which kind of role it is |
| 7 Employer | Class the user deprioritized | Label it explicitly |
| 8 Culture | Matches a listed red-flag phrase | Flag prominently |
| 9 Dedupe | Company plus role already seen or applied | Silent drop, log it |
| 10 Link | URL cannot be confirmed to resolve to the posting | Link the job board instead, or say it is unverified |
