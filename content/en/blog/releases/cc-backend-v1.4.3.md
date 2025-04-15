---
title: Release cc-backend v1.4.3
date: 2025-03-14T00:00:00.000Z
description: Bugfix Release
---

## Changelog

### New features

- feat: add deselect all button to jobStatefilter
- feat: add subCluster level frontend keys for metric selections

### Bug fixes

- fix: Do not allow to start a job with a state != running
- fix: Fix go version in go.mod
- fix: add missing exclusive filter handler for jobQuery
- fix: add missing factor for job power calculation, see Issue [#340](https://github.com/ClusterCockpit/cc-backend/issues/340)
- fix: add missing parameters for correct shared metric thresholds
- fix: analysis view top links fixed, add full name to topusers
- fix: decouple polarPlot data query, add new dedicated gql endpoint
- fix: fix svelte js race condition on metric selection change, see Issue [#335](https://github.com/ClusterCockpit/cc-backend/issues/335)
- fix: load jobView roofline on finest resolution separately by default, see Issue [#339](https://github.com/ClusterCockpit/cc-backend/issues/339)
- fix: remove caching for footprint db field
- fix: separate polar plot metric list from job.footprint return
- fix: use job_view_selectedMetrics config instead of iterating globalMetrics
- fix: user and status view histogram selection

## Release notes

This is a bugfix release of `cc-backend`, the API backend and frontend
implementation of ClusterCockpit.

Supports job archive version 2 and database version 8.
Please check out the [Release Notes](https://github.com/ClusterCockpit/cc-backend/blob/master/ReleaseNotes.md) for further details on breaking changes.

## Known issues

- Currently energy footprint metrics of type energy are ignored for calculating
  total energy.
- Resampling for running jobs only works with cc-metric-store
- With energy footprint metrics of type power the unit is ignored and it is
  assumed the metric has the unit Watt.

## Download

[Download the release on GitHub!](https://github.com/ClusterCockpit/cc-backend/releases/tag/v1.4.3)
