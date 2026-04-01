---
title: Developer git Workflow
description: >
  How the ClusterCockpit team is using GitHub Flow with git rebase.
weight: 80
tags: [Developer]
---

## Overview

ClusterCockpit uses **GitHub Flow**: `main` is always deployable, all work
happens on short-lived feature branches, and every change lands via a pull
request. History is kept linear by rebasing — no merge commits from feature
branches.

| Branch         | Purpose                                                          |
| -------------- | ---------------------------------------------------------------- |
| `main`         | Active development; source for the next release                  |
| `release/v1.x` | Persistent; created per minor release, receives backported fixes |

**External contributors** fork the repository and add the upstream as a second
remote. **Core team members** clone upstream directly and replace `upstream`
with `origin` in the commands below.

### One-time git configuration

```bash
git config --global pull.rebase true
```

---

## Branch Naming

```
<type>/<issue-number>-<short-description>
```

| Prefix  | Use for       |
| ------- | ------------- |
| `feat/` | New features  |
| `fix/`  | Bug fixes     |
| `doc/`  | Documentation |

Examples: `feat/123-auto-job-tagging`, `fix/backport-423-wal-rotation-v1.3`

Persistent release branches: `release/v1.x` (minor version only).

---

## Development Cycle

1. **Sync** `main` before starting:

   ```bash
   git pull
   ```

2. **Branch** off `main`:

   ```bash
   git checkout -b feat/123-my-feature main
   ```

3. **Commit** freely — informal messages are fine during development; they will
   be cleaned up before the PR. Reference issue numbers where relevant.

4. **Push**, and use optionally `--force-with-lease` (never `--force`) after any
   rebase:

   ```bash
   git push -u origin feat/123-my-feature
   git push --force-with-lease origin feat/123-my-feature  # after rebase
   ```

5. **Rebase onto `main`** whenever the base branch has moved to ensure feature
   branch is compatible with latest upstream main:

   ```bash
   git fetch origin && git rebase origin/main
   ```

---

## Optional: Interactive Rebase Before Opening a PR

Clean up the branch history so each commit is a logical unit with a proper
prefix message before requesting review:

```bash
git rebase -i upstream/main
```

Squash WIP commits with `squash` / `fixup`, polish messages with `reword`.
See [Commit Message Conventions]({{< ref "commit-messages" >}}) for the
required prefixes. Push with `--force-with-lease` afterwards.

---

## Pre-PR Checklist

- [ ] Rebased on current `main`, no merge commits in the branch
- [ ] Commit messages follow prefix conventions
- [ ] Issue number referenced in a commit message or PR description
- [ ] Docs updated if user-facing behaviour changed (see [Contributing to Documentation]({{< ref "documentation" >}}))

---

## Pull Requests

Target `main` for new work; target `release/v1.x` for backports.

- **Title**: use commit prefix conventions (`feat: …`, `fix: …`)
- **Description**: what and why; how to test; closing keyword (`Fixes #423`)
- Use GitHub **Draft** status for work in progress
- Keep PRs small

---

## Reference

- [Commit Message Conventions]({{< ref "commit-messages" >}}) — prefix tags, issue linking, goreleaser integration
- [Unit Tests]({{< ref "testing" >}}) — Go test conventions and `make test`
- [Frontend Development Setup]({{< ref "frontend-testing" >}}) — Svelte/npm workflow for cc-backend
- [Contributing to Documentation]({{< ref "documentation" >}}) — Hugo setup and local preview
- [Preparing a Release]({{< ref "release" >}}) — release branches, tagging, goreleaser, backporting
