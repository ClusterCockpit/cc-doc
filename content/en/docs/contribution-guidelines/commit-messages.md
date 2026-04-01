---
title: Commit Message Conventions
weight: 10
description: Prefix tags for release notes, issue linking, and goreleaser integration
tags: [Developer]
---

## Introduction

ClusterCockpit uses [goreleaser](https://goreleaser.com/) for building and
uploading releases. Release notes are generated automatically from commit
messages using the prefix tags described below. GitHub also parses special
keywords to link commits and PRs to issues.

Before opening a pull request, use [interactive rebase]({{< ref "_index#interactive-rebase----cleaning-up-before-a-pr" >}})
to clean up your branch history and ensure the final commit messages follow
these conventions.

---

## Release Note Prefixes

Commits carrying one of the following prefixes appear in the generated release
notes:

| Prefix  | Appears under         |
| ------- | --------------------- |
| `feat:` | New features          |
| `fix:`  | Bug fixes             |
| `doc:`  | Documentation updates |

Commits without a recognised prefix are not included in the release notes.

**Examples:**

```
feat: add automatic job tagging
fix: correct WAL rotation on partial flush (#423)
doc: update rebase workflow guide
```

---

## Referencing Issues

It is good practice to create a GitHub issue for any notable change so that
the motivation and discussion are preserved. Reference an issue in any commit
message or PR description using the `#<number>` syntax:

```
This change contributes to #235
```

---

## Automatically Closing Issues

GitHub closes an issue automatically when a PR containing one of the following
keywords merges into the default branch:

- `close`, `closes`, `closed`
- `fix`, `fixes`, `fixed`
- `resolve`, `resolves`, `resolved`

The issue is not closed until the commit appears on `main`. Example:

```
fix: correct WAL rotation on partial flush

Fixes #423
```

Place the closing keyword in the PR description rather than a WIP commit
message, since commit messages are often rewritten with interactive rebase
before the PR is merged.
