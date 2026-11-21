# Adapted skills

Some skills here adapt work by other people. Each one says so, and the repo check enforces it.

## How a skill is marked

1. Add `adapted_from:` to the skill's frontmatter. Say where it came from: the author and repo, or the URL.
2. End `SKILL.md` with one `Source:` line. It starts with the author, then gives a link to the original, then the license.

```md
Source: Matt Pocock, [mattpocock/skills](https://github.com/mattpocock/skills) (grilling), MIT license.
```

## What the check enforces

`tests/checks_adapted.py` fails when:

- a skill with `adapted_from:` does not end with a `Source:` line
- the line has no author, no link, or no cleared license (today: MIT)
- a skill names Matt Pocock or Pawel Huryn but has no `adapted_from:`

Add a license to `ADAPT_LICENSES` only after you read its terms.

## Who we adapt, and who we only name

- Matt Pocock and Pawel Huryn publish under MIT. We may adapt their skills with the line above.
- Aakash Gupta and 90n: name and link only. Never copy their text.
