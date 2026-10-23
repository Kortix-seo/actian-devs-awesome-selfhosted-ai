# Maintainers

## Description rewrite before sindresorhus submission

Every entry description (the `description` field in `data/entries/*.yml`) is a factual draft written for scaffolding. Before submitting this list to [sindresorhus/awesome](https://github.com/sindresorhus/awesome), a human on the team must rewrite each description. Fully AI-generated list content is rejected by sindresorhus/awesome and by awesome-selfhosted.

Suggested process:

1. Freeze the entry set.
2. Split categories among maintainers.
3. Rewrite each one-sentence description in a human voice, in the entry's YAML file.
4. Run `python3 scripts/validate.py`, `python3 scripts/build_readme.py`, `npx awesome-lint`, and the link checker.
5. Wait until the repo has been public for at least 30 days, then open the Awesome PR.

## Weekly snapshot PRs

The `snapshot` workflow opens a PR each Monday. Review it, merge it so the history is kept, and open follow-up PRs to remove archived or stale entries under the removal policy in CONTRIBUTING.md.

## Owners

- [@xamfonos](https://github.com/xamfonos)

## Owners still to add

- Actian developer community maintainers (merge rights): @handle-tbd, @handle-tbd
- Hackmamba collaborators during the launch window: @handle-tbd

Replace each `@handle-tbd` with a real GitHub handle before public launch.
