---
title: Preparing a Release
description: >
  How to cut new releases and backport fixes using persistent release branches
  and goreleaser.
weight: 50
tags: [Developer]
---

## Branch Model

ClusterCockpit maintains two types of long-lived branches:

| Branch | Purpose |
|---|---|
| `main` | Active development; all new features and fixes land here first |
| `release/v1.x` | Persistent branch for a minor release series; receives backported fixes |

A `release/v1.x` branch is created once when cutting a new minor or major
release and stays open indefinitely. All `v1.x.y` patch releases are tagged
from this branch. Short-lived fix branches for backports are PRed into the
release branch, not into `main`.

Every change — including urgent fixes — follows the same feature-branch/PR
workflow described in the [Developer Workflow]({{< ref "_index" >}}) guide.
There is no "hotfix directly to main" shortcut.

---

## Cutting a New Minor or Major Release

### 1. Prepare `main`

Ensure all PRs intended for the release are merged and CI is green on `main`.

### 2. Create the release branch

```bash
git checkout main
git pull --rebase
git checkout -b release/v1.x
git push -u origin release/v1.x
```

### 3. Bump the version

On a short-lived branch from `release/v1.x`, update the version in `Makefile`
and prepare `ReleaseNotes.md`:

```bash
git checkout -b doc/release-v1.x.0 release/v1.x
# edit Makefile and ReleaseNotes.md
git add Makefile ReleaseNotes.md
git commit -m "doc: prepare release v1.x.0"
git push -u origin doc/release-v1.x.0
```

Open a PR targeting `release/v1.x` (not `main`), get it reviewed, and merge.

### 4. Tag the release

On a Linux host with repository push access:

```bash
git fetch origin
git checkout release/v1.x
git pull --rebase
git tag v1.x.0 -m "release v1.x.0"
git push origin v1.x.0
```

### 5. Run goreleaser

Ensure the `GITHUB_TOKEN` environment variable is set, then:

```bash
goreleaser release
```

goreleaser builds the release artifacts, generates release notes from commit
prefixes, and publishes everything to the GitHub Releases page. See
[Commit Message Conventions]({{< ref "commit-messages" >}}) for the prefix
tags that control what appears in the release notes.

### 6. Post-release

- Verify the release appears correctly on the GitHub Releases page.
- Close the milestone for this release if one was used.
- Announce the release in the appropriate channels.

---

## Patch Releases — Backporting Fixes

Patch releases (`v1.x.1`, `v1.x.2`, …) are cut from the `release/v1.x`
branch after backporting one or more fixes from `main`.

### 1. Develop the fix on `main` first

Follow the standard feature-branch workflow and merge the fix into `main` via
a PR. Note the commit SHA(s) of the fix once merged.

### 2. Create a backport branch

```bash
git fetch origin
git checkout release/v1.x
git pull --rebase
git checkout -b fix/backport-<issue>-<description>
```

### 3. Cherry-pick the fix

```bash
git cherry-pick <commit-sha>
```

If the cherry-pick produces conflicts, resolve them, stage the files, then
continue:

```bash
git add <resolved-files>
git cherry-pick --continue
```

### 4. Open a PR targeting the release branch

```bash
git push -u origin fix/backport-<issue>-<description>
```

Open the PR on GitHub and set the **base branch** to `release/v1.x`, not
`main`. The PR description should reference the original issue and the commit
SHA that was cherry-picked.

### 5. Tag the patch release

After the backport PR is merged:

```bash
git fetch origin
git checkout release/v1.x
git pull --rebase
git tag v1.x.1 -m "release v1.x.1"
git push origin v1.x.1
goreleaser release
```

Repeat steps 2–5 for each additional fix that needs to be included in the
patch release before tagging.
