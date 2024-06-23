---
title: Release cc-backend v1.3.1
date: 2024-06-22T00:00:00.000Z
description: Bugfix Release
---
## Changelog

### New Features

- ef51e69 feat: Add roofline color scale for time information
- 5757530 feat: add jobname filter to joblist textfilter
- 72557fd feat: add statistics series render to job view metric plots
- 8d1228c feat: rework list searchbar, adds project-specific mode, add to user-joblist

### Bug fixes

- 54f7980 fix: Add required key to init config file
- 597bccc fix: add SQL JSON validity check to meta_data query
- 320c87a fix: add additional 30d fitler to searchbar fallback handling
- a4397d5 fix: add scramble to textfilter component
- 70e6376 fix: allow single partial errors on otherwise non-empty returned metric array
- ba1658b fix: correct selectable histogram placement in status view
- b48d1b8 fix: correct status view columns on mobile displays
- 061c9f0 fix: deselected metrics were marked as missing on new jobview load
- 420bec7 fix: fix jobname and arrayjobid timeouts by adding additional 30d filter
- c9eb40f fix: fix metricPlot y zoom reset
- cbaeffd fix: improve speed of hasNextPage query for infinite scroll
- 4344c26 fix: make foorprint from statsSeries nullsafe

Supports job archive version 1 and database version 6.
Please check out the [Release Notes](https://github.com/ClusterCockpit/cc-backend/blob/master/ReleaseNotes.md) for further details on breaking changes.

## Release notes

This is a bugfix release of `cc-backend`, the API backend and frontend
implementation of ClusterCockpit.

### Breaking changes

None

## Download

[Download the release on GitHub!](https://github.com/ClusterCockpit/cc-backend/releases/tag/v1.3.1)

