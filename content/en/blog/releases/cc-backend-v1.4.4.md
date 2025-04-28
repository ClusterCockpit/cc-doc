---
title: Release cc-backend v1.4.4
date: 2025-04-28:00:00.000Z
description: Bugfix Release
---

## Changelog

### New Features

* feat: add nodename matcher select to filter, defaults to equal match
* feat: add remove functionality to tag view, add confirm alert
* feat: add tag removal api endpoints

### Bug fixes

* fix: Replace deprecated gqlgen NewDefaultServer call
* fix: Update endpoints in Swagger UI
* fix: add name scrambling demo mode to all views
* fix: add nullSafe condition to monitoringStatus display on metric queryError
* fix: always return hasNextPage boolean to frontend
* fix: correct logging variable from err to ipErr in AuthApi
* fix: enforce apiAllowedIPs config option
* fix: fix error in jobsMetricStatisticsHistogram calculation
* fix: fix nodelist filter result displaying wrong information
* fix: reintroduce statstable id natural sort order

### Release notes

This is a bugfix release of `cc-backend`, the API backend and frontend
implementation of ClusterCockpit.

Supports job archive version 2 and database version 8.
Please check out the [Release Notes](https://github.com/ClusterCockpit/cc-backend/blob/master/ReleaseNotes.md) for further details on breaking changes.

## Breaking changes

The option `apiAllowedIPs` is now a required configuration attribute in
`config.json`. This option restricts access to the admin API.

To retain the previous behavior that the API is per default accessible from
everywhere set:

```json
  "apiAllowedIPs": [
    "*"
  ]
```

## Known issues

* Currently energy footprint metrics of type energy are ignored for calculating
  total energy.
* Resampling for running jobs only works with cc-metric-store
* With energy footprint metrics of type power the unit is ignored and it is
  assumed the metric has the unit Watt.

## Download

[Download the release on GitHub!](https://github.com/ClusterCockpit/cc-backend/releases/tag/v1.4.4)
