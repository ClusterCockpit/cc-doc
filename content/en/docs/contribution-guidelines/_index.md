---
title: Developer Workflow
description: >
  End-to-end guide for contributing to ClusterCockpit using GitHub Flow
  with git rebase for a clean, linear history.
weight: 80
tags: [Developer]
---

## Overview

ClusterCockpit uses a **GitHub Flow** variant: `main` is always in a deployable
state, all development happens on short-lived feature branches, and every change
lands via a pull request (PR). A linear git history is maintained by rebasing
instead of merging — there are no merge commits from feature branches.

Two persistent branch types exist alongside the short-lived work branches:

| Branch | Purpose |
|---|---|
| `main` | Active development; source for the next release |
| `release/v1.x` | Long-lived; created when cutting a minor/major release, receives backported fixes |

Two contributor models are supported:

- **External contributors** fork the repository on GitHub and work on branches
  inside their fork.
- **Core team members** work on branches directly in the upstream repository.

The PR-based code review step is identical for both paths.

---

## Prerequisites

- **Git 2.x** — the workflow uses `--rebase`, `--autostash`, and interactive rebase
- **GitHub account** with access to the relevant ClusterCockpit repository
- Language toolchains for the component you are working on:
  - Go 1.25+ for backend components — see [Getting Started]({{< ref "/docs/getting-started" >}})
  - Node.js + npm for the web frontend — see [Frontend Development Setup]({{< ref "frontend-testing" >}})
  - Hugo extended for documentation — see [Contributing to Documentation]({{< ref "documentation" >}})

Configure git to rebase by default whenever you pull, and to stash local
changes automatically during a rebase:

```bash
git config --global pull.rebase true
git config --global rebase.autoStash true
```

---

## Repository Setup

### External contributors — fork model

1. Fork the repository on GitHub (e.g. `ClusterCockpit/cc-backend`).

2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/cc-backend.git
   cd cc-backend
   ```

3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/ClusterCockpit/cc-backend.git
   ```

4. Verify:
   ```bash
   git remote -v
   # origin    https://github.com/<your-username>/cc-backend.git (fetch)
   # origin    https://github.com/<your-username>/cc-backend.git (push)
   # upstream  https://github.com/ClusterCockpit/cc-backend.git (fetch)
   # upstream  https://github.com/ClusterCockpit/cc-backend.git (push)
   ```

5. Never commit directly to your fork's `main`. Keep it as a clean mirror of
   upstream and always work on named branches.

### Core team members — direct clone

1. Clone the upstream repository:
   ```bash
   git clone https://github.com/ClusterCockpit/cc-backend.git
   cd cc-backend
   ```

2. There is a single `origin` remote pointing to upstream. Push branches to
   `origin` and open PRs from there.

In the commands that follow, core team members replace `upstream` with `origin`.

---

## Branch Naming Conventions

Short-lived work branches follow this format:

```
<type>/<issue-number>-<short-description>
```

The type mirrors the [commit message prefix conventions]({{< ref "commit-messages" >}}):

| Prefix | Use for |
|---|---|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `sec/` | Security fixes |
| `doc/` | Documentation changes |
| `fix/backport-` | Backports of fixes to a release branch |

**Examples:**

```
feat/123-auto-job-tagging
fix/423-wal-rotation-partial-failure
sec/512-api-token-expiry
doc/rebase-workflow-guide
fix/backport-423-wal-rotation-v1.3
```

Persistent release branches are named `release/v1.x` (minor version only, no
patch number — the branch spans all `v1.x.y` patch releases).

Avoid generic names like `my-changes`, `patch`, or `wip`.

---

## Daily Development Workflow

### Step 1 — Sync with upstream before starting

External contributors:
```bash
git fetch upstream
git checkout main
git rebase upstream/main
git push origin main          # keep your fork's main up to date
```

Core team:
```bash
git fetch origin
git checkout main
git rebase origin/main
```

### Step 2 — Create a feature branch

Always branch off from `main`:

```bash
git checkout -b feat/123-my-feature main
```

### Step 3 — Develop and commit

Make small, focused commits as you work. Messages during development can be
informal — they will be cleaned up with interactive rebase before the PR is
opened. Reference issue numbers in commit messages or the PR description.
See [Commit Message Conventions]({{< ref "commit-messages" >}}) for the
prefix rules that apply to the final commit messages.

### Step 4 — Push your branch

```bash
git push -u origin feat/123-my-feature
```

After any subsequent rebase, push with `--force-with-lease` (never bare
`--force`, which can silently overwrite collaborators' pushes):

```bash
git push --force-with-lease origin feat/123-my-feature
```

---

## Keeping Your Branch Up to Date

While your branch is open, `main` may receive other commits. Rebase rather
than merging to keep the history linear.

External contributors:
```bash
git fetch upstream
git rebase upstream/main
```

Core team:
```bash
git fetch origin
git rebase origin/main
```

When conflicts occur, git pauses at each conflicting commit. Resolve the
conflict, stage the resolved files, then continue:

```bash
# edit conflicting files, then:
git add <resolved-files>
git rebase --continue
```

To abandon the rebase and restore the pre-rebase state:

```bash
git rebase --abort
```

After rebasing a branch that was already pushed, a force-push is required:

```bash
git push --force-with-lease origin feat/123-my-feature
```

If others are collaborating on your branch, coordinate with them before
force-pushing.

---

## Interactive Rebase — Cleaning Up Before a PR

Before opening a PR, use interactive rebase to clean up the branch history so
each commit represents a logical, self-contained change with a proper commit
message.

```bash
git rebase -i upstream/main    # or origin/main for core team
```

This opens an editor listing every commit on your branch since it diverged
from `main`. Available actions:

| Action | Effect |
|---|---|
| `pick` | Keep commit as-is |
| `reword` | Keep commit, edit its message |
| `squash` | Fold into the previous commit, combine messages |
| `fixup` | Fold into the previous commit, discard this message |
| `drop` | Remove the commit entirely |

**Example** — squash four WIP commits into one clean commit:

```
pick a1b2c3 feat: initial skeleton for job tagging
squash d4e5f6 wip: add tagger logic
fixup 7g8h9i typo
fixup j0k1l2 add test
```

After saving, git prompts you to edit the combined commit message. Apply the
`feat:` / `fix:` prefix conventions here. Then push:

```bash
git push --force-with-lease origin feat/123-my-feature
```

---

## Pre-PR Checklist

Before opening a pull request, verify:

- [ ] Branch is rebased on current `main` — no merge commits in the branch
- [ ] All commits carry proper prefix messages (see [Commit Message Conventions]({{< ref "commit-messages" >}}))
- [ ] Go tests pass locally: `make test` (see [Unit Tests]({{< ref "testing" >}}))
- [ ] Frontend build passes if frontend files were changed: `npm run build` (see [Frontend Development Setup]({{< ref "frontend-testing" >}}))
- [ ] No debug output, commented-out code, or temporary scaffolding is committed
- [ ] Branch name follows the naming conventions above
- [ ] The relevant issue number is referenced in at least one commit message or the PR description
- [ ] Documentation is updated if the change affects user-facing behaviour (see [Contributing to Documentation]({{< ref "documentation" >}}))

---

## Creating and Managing Pull Requests

Open a PR from your branch against `ClusterCockpit/<repo>/main` (or against a
`release/v1.x` branch for backports — see [Preparing a Release]({{< ref "release" >}})).

**PR title** — follow the same commit prefix conventions:

```
feat: add automatic job tagging
fix: correct WAL rotation on partial flush
```

**PR description** should include:

- What the change does and why
- How to test or reproduce the scenario
- The issue number using a closing keyword so GitHub links and closes it automatically:
  ```
  Fixes #423
  ```
  See [Commit Message Conventions]({{< ref "commit-messages" >}}) for the full list of accepted keywords.

**Practical guidelines:**

- Use GitHub's **Draft** status while work is in progress instead of adding
  "WIP" to the title.
- Add reviewers explicitly — do not leave the reviewer field empty.
- Keep PRs small and focused. Split large changes into a series of dependent
  PRs when possible.
- Address all review comments before requesting re-review.

---

## Code Review Process

### For reviewers

- Review the diff, not the developer. Keep comments constructive and specific.
- Distinguish blocking concerns from suggestions — use **Request changes** only
  for issues that must be addressed before merge.
- Check: does the code do what the PR description says? Do tests cover the
  change? Are commit messages correct?

### For authors

- Address all review comments, either by making changes or by explaining why
  no change is needed.
- After addressing feedback, push updated commits to the branch. Coordinate
  with the reviewer whether to add new commits or to amend/rebase and
  force-push — either approach is acceptable, but agree first.
- Use the **Re-request review** button when ready for another look.
- Do not resolve the reviewer's comment threads yourself; let the reviewer
  dismiss their own requests.

---

## Merging

Only maintainers merge PRs into `main` or `release/v1.x`.

The preferred merge strategy is **Rebase and merge**: it replays the branch's
commits on top of the target branch without a merge commit, preserving the
linear history. Because authors clean up commits with interactive rebase before
opening the PR, the rebased commits are already in final form.

After merge:
- GitHub closes the linked issue automatically if the PR description used a
  closing keyword (`Fixes #N`, `Closes #N`, etc.).
- The merged branch is deleted from the remote immediately — enable this in
  GitHub repository settings (*Automatically delete head branches*).

---

## After Merge Cleanup

Sync your local `main`:

External contributors:
```bash
git fetch upstream
git checkout main
git rebase upstream/main
git push origin main
```

Core team:
```bash
git fetch origin
git checkout main
git rebase origin/main
```

Delete the local feature branch:

```bash
git branch -d feat/123-my-feature
```

Use `-D` instead of `-d` only if the branch was squash-merged and git reports
it as unmerged. If the remote branch was not deleted automatically:

```bash
git push origin --delete feat/123-my-feature
```

You are now ready to start the next feature. Return to
[Daily Development Workflow](#daily-development-workflow).

---

## Reference

The pages in this section cover topic-specific details that apply within the
workflow described above:

- [Commit Message Conventions]({{< ref "commit-messages" >}}) — prefix tags, issue linking, goreleaser integration
- [Unit Tests]({{< ref "testing" >}}) — Go test conventions and how to run the test suite locally
- [Frontend Development Setup]({{< ref "frontend-testing" >}}) — Svelte/npm workflow for cc-backend
- [Contributing to Documentation]({{< ref "documentation" >}}) — Hugo setup, local preview, Docsy conventions
- [Preparing a Release]({{< ref "release" >}}) — release branches, tagging, goreleaser, backporting
