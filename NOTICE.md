# Third-party notices

Everything in this repository is MIT licensed (see [LICENSE](LICENSE)). Almost all of it is
original work by the repository author. This file records the exceptions and the
attributions, skill by skill.

## Summary

| Skill | Origin |
|-------|--------|
| `latam-job-search` | Skill definition original. **Bundled CLIs are third-party**, see below. |
| `project-setup`, `dev`, `test`, `review`, `deep-review`, `ux`, `deploy`, `ship`, `product`, `community-manager` | Rewritten by the author from a private single-project skill set |
| `feature-agents`, `deploy-qa`, `decision-log`, `design-system`, `linkedin-personal-brand` | Original |

## latam-job-search: bundled CLIs

The two portal CLIs under `latam-job-search/tools/` (`linkedin-search` and
`freehire-search`) originate from the **ai-job-search** framework by Mads Lorentzen,
distributed under the MIT License:

> https://github.com/MadsLorentzen/ai-job-search

```
MIT License

Copyright (c) 2026 Mads Lorentzen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

The skill definition around them (`SKILL.md`, everything under `references/` and `assets/`)
is original work.

### Terms of service

`linkedin-search` reads LinkedIn's public `jobs-guest` pages. Automated access to LinkedIn
is against their Terms of Service. The CLI is provided for **personal use at low volume**
only; do not use it commercially or for bulk data collection. You run it on your own
responsibility.

## Skills rewritten from a private set

`project-setup`, `dev`, `test`, `review`, `deep-review`, `ux`, `deploy`, `ship`, `product`
and `community-manager` were rewritten by the repository author from a private,
single-project skill set. The originals were hardcoded to one codebase and one product;
these versions are configuration-driven and carry no project-specific data. Same author,
same MIT license, no third-party rights involved.

## Original skills

`feature-agents`, `deploy-qa`, `decision-log`, `design-system` and
`linkedin-personal-brand` are original work by the repository author, written for this
collection.

## Inspirations

Ideas that shaped a skill's format, none of which involve copied material:

- `deep-review`'s interactive options-and-tradeoffs format was inspired by a code review
  style publicly associated with Garry Tan. The interpretation and all text are original.
- `decision-log` is a lightweight take on the Architecture Decision Record pattern
  popularised by Michael Nygard. The format here is deliberately smaller and the text is
  original.

## What none of these do

No skill in this repository transmits your data anywhere, bundles a tracker, or requires an
account, an API key or a login. The only network access any of them make is the job-portal
CLIs above, plus ordinary web search and fetch when a skill explicitly says it is verifying
something.
