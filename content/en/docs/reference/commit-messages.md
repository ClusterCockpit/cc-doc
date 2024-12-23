---
title: Commit message naming conventions
weight: 90
description: Special keywords to reference tickets and control release notes
tags: [Developer]
---
## Introduction

ClusterCockpit uses [goreleaser](https://goreleaser.com/) for building and
uploading releases. In this process the release notes including all notable
changes are automatically generated based on special commit message tags.
Moreover GitHub will parse special characters and words to link and close
issues.

## Reference issue tickets

It is good practice to always create a ticket for notable changes.
This allows to comment and discuss about source code changes. Any commit that
contributes to the ticket should reference the ticket id (in the commit message
or description). This is achieved in GitHub by prefixing the ticket id with a
number sign character (`#`):

```txt
This change contributes to #235
```

GitHub will detect if a pull request or commit uses special keywords to close a
ticket:

- close, closes, closed
- fix, fixes, fixed
- resolve, resolves, resolved

The ticket will not be closed before the commit appears on the main branch.
Example:

```txt
This change fixes #423
```

## Control release notes with preconfigured commit message prefixes

Commits with one of the following prefixes will appear in the release notes:

- **feat:** Mark a commit to contain changes related to new features
- **fix:** Mark a commit to contain changes related to bug fixes
- **sec:** Mark a commit to contain changes related to security fixes
- **doc:** Mark a commit to contain changes related to documentation updates
- **[feat|fix] dep:** Mark a commit that is related to a dependency introduction
  or change
