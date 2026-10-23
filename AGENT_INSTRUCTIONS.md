# Instructions for the coding agent (VS Code / Cursor)

Henry Bassey wants you to **create** the public GitHub repository and **push this scaffold as the initial commit**. Do not invent a different structure; use these files as-is unless a link is broken.

## Goal

Create and publish:

**https://github.com/actian-devs/awesome-selfhosted-ai**

Org: [actian-devs](https://github.com/actian-devs) (Actian for Developers)  
Visibility: **public**  
Default branch: **main**

## What this folder is

Exhaustive Awesome list of self-hosted AI tools (179 entries, 15 categories plus Related), plus contribution docs and CI.

| File | Purpose |
|---|---|
| `README.md` | The list (do not rename heading `# Awesome Self-Hosted AI`) |
| `CONTRIBUTING.md` | Inclusion rules, format, PR process |
| `LICENSE` | CC0-1.0 (required for sindresorhus/awesome) |
| `MAINTAINERS.md` | Humans must rewrite AI-drafted descriptions before sindresorhus submission |
| `code-of-conduct.md` | Contributor Covenant 2.1 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR checklist |
| `.github/workflows/lint.yml` | `awesome-lint` on PR/push |
| `.github/workflows/links.yml` | Weekly dead-link check (lychee) |
| `BUILD_NOTES.md` | Scaffold metadata (optional to keep; fine to leave in repo) |
| `AGENT_INSTRUCTIONS.md` | This file (you may delete after push, or keep) |

## Step-by-step

### 1. Prerequisites

- Logged into GitHub as a user who can create repos in **actian-devs**.
- `gh` authenticated (`gh auth status`), or use the GitHub UI / VS Code GitHub extension with the same access.
- Git identity set (`git config user.name` / `user.email`).

### 2. Create the empty public repository

Prefer CLI:

```bash
gh repo create actian-devs/awesome-selfhosted-ai \
  --public \
  --description "Exhaustive curated list of self-hosted AI tools: models, inference, embeddings, vector databases, agents, evals, GPUs and deploy." \
  --disable-wiki \
  --clone=false
```

If the org requires a team or you lack permission, stop and tell Henry. Do not create it under a personal account.

Optional topics after create (GitHub UI or API):

`awesome`, `awesome-list`, `self-hosted`, `local-llm`, `vector-database`, `rag`, `ai-agents`

### 3. Initialize git from this folder and push

Run from the directory that contains this `AGENT_INSTRUCTIONS.md` (the scaffold root):

```bash
cd "$(dirname "$0")"   # or: cd /path/to/awesome-selfhosted-ai

git init -b main
git add README.md CONTRIBUTING.md LICENSE MAINTAINERS.md code-of-conduct.md \
  .github BUILD_NOTES.md lychee.toml
# Optionally include AGENT_INSTRUCTIONS.md, or omit/delete it before commit
git add AGENT_INSTRUCTIONS.md 2>/dev/null || true

git commit -m "Initial commit: Awesome Self-Hosted AI (179 entries, 15 categories)"

git remote add origin git@github.com:actian-devs/awesome-selfhosted-ai.git
# HTTPS alternative:
# git remote add origin https://github.com/actian-devs/awesome-selfhosted-ai.git

git push -u origin main
```

If `main` is protected or the remote already has a README from the GitHub UI wizard, pull/rebase or force only if Henry confirms. Prefer an **empty** repo with no README/license from the wizard.

### 4. Verify

- Open https://github.com/actian-devs/awesome-selfhosted-ai
- Confirm README renders, Contents ToC works, Discord badge links to `https://discord.gg/t26wZw22X`
- Confirm Actions tabs show `lint` and `links` workflows
- Spot-check: VectorAI DB is alphabetical under Vector databases and tagged `⊘ Proprietary`
- Spot-check: Memory Hub and vector-db-calculator entries point at actian-devs repos

### 5. After push (tell Henry)

Report back:

1. Live URL of the repo
2. Whether create + push succeeded
3. Any files you changed (ideally none)
4. Whether GitHub Actions ran / failed

Henry will then: mint Discord per-source invites, have humans rewrite descriptions (see `MAINTAINERS.md`), and plan the Nov launch. Do **not** submit to sindresorhus/awesome yet (needs 30 days live + human descriptions).

## Hard rules (do not violate)

- **Do not** pin, bold, or badge VectorAI DB above peers.
- **Do not** add Actian marketing blog posts as software entries.
- **Do not** put UTM or bki.sh tracking links inside list entry URLs.
- **Do not** change the list license away from CC0-1.0.
- **Do not** rewrite all descriptions with another LLM pass “to polish” — that fights sindresorhus rules; leave drafts for human rewrite.
- Keep entry format: `- [Name](url) - Description ending with a period.`
- Keep alphabetical order within each category.

## Product / tracking context (for humans, not for README body)

- Org Discord base invite: https://discord.gg/t26wZw22X (create per-source invite codes later)
- Calculator: https://github.com/actian-devs/vector-db-calculator
- Memory Hub: https://github.com/actian-devs/agent-memory-hub
- Plan / research live in Henry’s Grok Bot Pages (not required for the push)

## Done when

`https://github.com/actian-devs/awesome-selfhosted-ai` exists, is public, `main` has this scaffold, and you have reported the URL to Henry.
