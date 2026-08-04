# Onboarding interview

Run this the first time the skill is used, or whenever the user says `/job-setup`,
"reconfigure my job search", or the profile file is missing.

**Output:** a single file, `job-search/profile.md`, written from
`assets/candidate-profile.template.md`. Nothing else is created at setup time.

## How to run it

Ask in **rounds**, not as one 15-question wall. Use `AskUserQuestion` with concrete
options plus a free-text escape hatch, so the user can click through the common case in
under two minutes and still type something specific when the options do not fit.

Three rules that make or break this interview:

1. **Never infer an answer from another answer.** "Based in Buenos Aires" does not tell
   you which countries will hire them, what currency they want to be paid in, or whether
   they can take a hybrid role. Every gate below has produced a wasted application when it
   was assumed instead of asked.
2. **Ask for the number, not the vibe.** "Competitive salary" and "good English" are not
   filters. A floor in a named currency and a CEFR level are.
3. **Write down what the user refuses to answer.** An unanswered gate becomes
   `UNKNOWN, ask before applying` in the profile, never a silent default.

At the end, echo the profile back as a short summary and ask for one confirmation before
writing the file.

---

## Round 1: where you are and where you can work

This round decides which postings are even legal or physically possible. It is the single
highest-value round: most bad matches die here.

**Q1.1 Base location and timezone.**
Ask for city, country, and UTC offset. Store the offset numerically (for example
`UTC-3`), because every timezone-overlap judgement later is arithmetic against it.

**Q1.2 Work modality. This answer is a hard filter, and the user must be told so.**
Options: `Fully remote only` / `Remote, hybrid OK in my city` / `Hybrid or onsite in my
city` / `Open to relocation`.

Say the consequence out loud when you ask, in one line: *"If you pick fully remote, I will
drop hybrid postings entirely, including hybrid roles in your own city."* Users pick
"remote" meaning a preference and are then annoyed to be shown hybrids; users who genuinely
want the wider net will say so when they see the trade-off stated.

If they pick a hybrid option, ask **which city the office must be in** and record it
verbatim. This is the difference between a real option and an impossible one: a person can
only be physically present in one city, so "hybrid in Bogotá" is exactly as disqualifying
as "onsite in Bogotá" for someone in Santiago, no matter how good the rest of the fit is.

Store the answer as a machine-checkable field (`modality: remote_only`), not as prose, and
apply it in Gate 2 of `02-eligibility-and-location.md` before any scoring happens.

**Q1.3 Countries that can actually hire you.**
Do not ask "are you open to remote?". Ask which of these count as eligible, multi-select:

- My own country only
- LatAm-wide postings
- "Anywhere" / worldwide postings
- US-based companies hiring international contractors
- EU-based companies hiring international contractors
- Named extra countries (free text: citizenship, residency, existing work permit)

Then ask the inverse and record it as a hard fail list: **which locations are an automatic
no**, for example "any posting locked to a single country that is not mine", "anything
requiring relocation", "anything requiring a visa I do not hold".

**Q1.4 Timezone overlap tolerance.**
"What is the largest time difference you can work with day to day?" Options:
`±2h` / `±4h` / `±6h` / `Async only, no fixed overlap` / `No limit`.

Also ask whether there is a hard start or end time (school run, a second job, a co-founded
project). Record the acceptable working window in **their** local time, not the
employer's.

**Q1.5 Work authorization.**
Citizenship or permanent residency status relevant to the target countries, and any permit
that constrains hours or start date. This is a gate, not a scoring dimension: a posting
that requires citizenship or a security clearance the user does not hold is a hard stop,
reported with the quoted wording, never silently dropped.

---

## Round 2: money

Ask this early and get numbers. A comp mismatch found in round 2 of the interview costs
nothing; found in round 3 of a hiring process it costs weeks.

**Q2.1 Currency.** Which currency do you want to be paid in, and is payment in your local
currency acceptable? For many LatAm markets the honest answer is "USD only", and that
single answer disqualifies a whole class of domestically funded local employers. Record it.

**Q2.2 Three numbers, not one.** Ask for all three, monthly or annual (record which):

| Number | Meaning |
|--------|---------|
| **Target** | What you open with on a salary-expectations field |
| **Floor** | Below this you would only move for an exceptional company |
| **Walk-away** | Below this the answer is no, regardless of anything else |

**Q2.3 Anchor by class of employer.** The same person cannot ask the same number
everywhere, and quoting the top number at an employer that structurally cannot pay it just
removes them in the first screen. Ask for a target per class, defaulting to the Q2.2 target:

- US or global company paying in hard currency
- Regional or local employer paying in local currency
- Consultancy or staff-augmentation firm
- Staffing or recruiting intermediary (they take a cut, the band is lower)
- Equity-heavy or early-stage startup

**Q2.4 Employment type.** Multi-select: `Permanent employee` / `Full-time contractor` /
`B2B invoice` / `EOR or PEO arrangement` / `Part-time` / `Freelance project`. Note which are
unacceptable, and whether benefits (health, PTO, equipment) change the acceptable number.

---

## Round 3: languages

This gate is chronically under-asked and it is where client-facing roles go wrong.

**Q3.1 Per language, a level and a split.** For each language the user speaks, record a
CEFR level (A1 to C2 or native) **and** whether written is stronger than spoken, or the
reverse. "Intermediate English, written stronger than spoken" is an actionable filter;
"good English" is not.

**Q3.2 The consequence question.** "If a job's day-to-day is live calls, discovery
sessions, or executive presentations in your second language, is that a stretch you want or
a risk you want filtered out?" Options: `Filter these out` / `Flag them, I will decide` /
`No problem, I want them`.

Record the answer, because it decides whether a posting demanding "fluent professional
English" for daily client delivery gets dropped or merely flagged.

---

## Round 4: the work itself

**Q4.1 Target role families, in priority order.** Let the user rank them; the order drives
which search queries run first. Offer their own titles plus free text.

**Q4.2 Hard exclusions.** This is the most useful question in the whole interview and the
one most setups omit. Ask outright: **which role types should never be shown to you, even
if the location and money are perfect?** Common answers worth offering as options:

- Roles with a title I want but no hands-on building content
- Pure process or program management with no product surface
- Deep specialist roles in a stack I do not have (name it)
- Live customer-facing or quota-carrying roles
- Roles at company types I do not want to work for (name them)

Store these as a **do-not-present** list. A skill that shows the user roles they already
said no to burns the user's trust faster than one that shows too few.

**Q4.3 Seniority reality.** Two numbers: years holding the formal target title, and total
years of relevant adjacent experience. Postings will ask for the first; the honest case is
usually made with the second. Record both so neither gets inflated later.

**Q4.4 Schedule shape.** Fixed hours vs flexible, on-call tolerance, and whether anything
outside the job (side project, studies, caregiving) needs protected hours. A role demanding
constant availability is a real deal-breaker for some people and irrelevant for others; do
not guess which.

---

## Round 5: skills and honesty boundaries

**Q5.1 Primary stack.** The tools and domains where the user is genuinely strong, in their
own words.

**Q5.2 Secondary stack.** Real but not deep. Useful for matching, dangerous to lead with.

**Q5.3 Never-claim list.** Ask explicitly: **what should never appear on a CV, cover
letter, or application form under your name, because you do not actually have it?** Record
verbatim. This list is a hard constraint on every document the skill later helps write, and
it is the difference between a tailored application and a fabricated one.

**Q5.4 Credentials in progress.** Degrees, certifications, or courses that are underway but
not finished. Record the true status. An in-progress credential is never marked complete on
a form, even under pressure to look more qualified, because unlike framing choices it is a
checkable claim.

---

## Round 6: companies, sectors and culture

Three separate questions here, and they are genuinely separate. Someone can want an early
startup and refuse consultancies, or want enterprise stability and refuse gambling. None of
it is inferable from the role title, and all of it changes what should be shown.

**Q6.1 Company type and stage.** Multi-select, and ask for each: `want` / `fine` /
`avoid`.

- Early-stage startup, pre-seed to Series A
- Scale-up, Series B and beyond
- Enterprise or large corporate
- PE or VC-owned portfolio company
- Consultancy or agency (you work on a client's product, and the client changes)
- Staffing or recruiting intermediary (the employer is undisclosed, the band is lower)
- Bootstrapped or small business
- Public sector, NGO or academic

Say the trade-off in one line so the answer is informed: an enterprise req usually means
more process and narrower scope, an early startup means more ambiguity and more surface
area. Neither is better; they are different jobs.

**Q6.2 Industries.** Two lists, and ask for both explicitly:

- Sectors the user **wants**, including any where they already have domain experience
  worth leading with (regulated industries, logistics, health, fintech, and so on).
- Sectors the user **refuses**. This is the one people are relieved to be asked. Offer the
  usual suspects as options (gambling, defence, adtech, crypto, tobacco, extractives, MLM,
  payday lending) plus free text. A refused sector is a hard drop, not a low score, and it
  will not change tomorrow.

**Q6.3 Exclude or label?** For each class marked `avoid` in Q6.1, ask whether it should be
excluded outright or shown with a label. Labeling is the better default for employer
relationship: a staffing role can be worth seeing as long as the user knows what it is
before they click. Excluding is the better default for refused sectors.

**Q6.4 Watch list.** Named companies to search every run, including ones the user admires
even if nothing is open right now. The daily run does a company-slug pass over these, and
any opening at one of them is worth surfacing even when the role differs from what they
asked for.

**Q6.5 Culture deal-breakers, in the posting's own words.** Ask for phrases that, if they
appear in a job description, should raise a flag. Real examples users have given: framing
internal confrontation as a virtue, "we thrive in chaos", "always on", "wear many hats" as
a euphemism for three unfilled roles. Store the phrases so the filter can grep for them.

---

## Round 7: output preferences

**Q7.1 Report language.** The language for the daily digest, which is often not the same as
the CV language.

**Q7.2 CV and application language.** Default, plus any market where it should differ.

**Q7.3 Volume and cadence.** How many postings per run, how far back to look (default 14
days), and whether the run should be daily, weekly, or on demand.

**Q7.4 Thin-day behaviour.** What should happen when the honest result is three matches,
not fifteen? Options: `Show me the three and say why the pool was thin` /
`Widen the search until you hit the target number` / `Include flagged near-misses, clearly labeled`.

The default is the first. Padding a list with postings that fail the user's own hard gates
is worse than a short list, because it teaches the user to stop reading the table.

---

## Closing the interview

Write `job-search/profile.md` from the template, then show a **six-line summary**: base and
modality, eligible locations, comp floor and currency, languages with levels, top three
target roles, and the do-not-present list. Ask the user to confirm or correct.

Then tell them the three commands that exist (`/job-search`, `/job-setup`,
`/job-track`) and stop. Do not run a search in the same turn as the setup: the user
just answered fifteen questions and a wall of results on top of that is not a reward.
