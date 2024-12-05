---
title: Release cc-backend v1.4.0
date: 2024-12-05T00:00:00.000Z
description: Minor Release
---

## Changelog

### New Features

- feat: Add buffered channel with worker thread for job start API
- feat: Add tag scopes to front and backend, initial commit
- feat: Add total energy and energy footprint
- feat: SyncUserOnLogin now updates name of token logged user
- feat: add configurability to frontend plot zoom
- feat: add dropdown to user and project list navbar
- feat: add edit of notice box content to admin settings
- feat: add updateUserOnLogin config option for oidc, jwt
- feat: change statistics render of metric plot to min/max/median
- feat: change to resolution increase on zoom
- feat: display energy usage in job view
- feat: make cron worker frequency configurable
- feat: make quick select starttimes url copyable
- feat: move tag management to new job view header
- feat: redirect to requested page after login, solves #281
- feat: split concurrent jobs list to own scrollable component

### Bug fixes

- fix: Replace reserved keywords in database schemas
- fix: SimpleResampler fixed
- fix: Update to resampler handling different resolutions
- fix: ad dmissing resampleConfig handling to scope select
- fix: add accelerator scope to to-be archived scopes
- fix: add additionally loaded scopes to statsTable again
- fix: add compatibility for footprint metrics without config
- fix: add missing default resolution case
- fix: add resolution 60 default to ccms nodeData query
- fix: archived statisticsSeries with mean data now shown again
- fix: errors in import paths
- fix: fix api test router init
- fix: fix crashing job view if roofline metrics missing
- fix: fix db migration to v8, changes key name to cpu_load
- fix: fix footprint logic, do not scale thresholds on multi node jobs
- fix: fix getMetricConfigDeep util function
- fix: fix job list render for continuous mode on filter or sort changes
- fix: fix plot labeling if specific host selected, hide loadall if only node returned
- fix: fix plot render for summed metrics on scope change
- fix: fix svelte source paths in makefile
- fix: fix tag filter results
- fix: fix wrongly inserted gql request and import path error
- fix: fixed and changed to footprint update by transactions
- fix: omit resources prop from metricPlot, use series for legend instead
- fix: oversight error on redirect target
- fix: prevent addition of existing scopes to table
- fix: prevent jump to table head on continuous scroll load
- fix: setup user in api test config
- fix: solve inconsistencies with filters, fixes #280
- fix: use configured footprint statType for update
- fix: use left join to keep unmatched stats query result rows
- fix: user name join not required for normal jobStats
- fix: wrong display of tag after filter select

## Release notes

This is a minor release of `cc-backend`, the API backend and frontend
implementation of ClusterCockpit.

Supports job archive version 2 and database version 8.
Please check out the [Release Notes](https://github.com/ClusterCockpit/cc-backend/blob/master/ReleaseNotes.md) for further details on breaking changes.

## Breaking changes

- You need to perform a database migration. Depending on your database size the
  migration might require several hours!
- You need to adapt the `cluster.json` configuration files in the job-archive,
  add new required attributes to the metric list and after that edit
  `./job-archive/version.txt` to version 2.
- Continuous scrolling is default now in all job lists. You can change this back
  to paging globally, also every user can configure to use paging or continuous
  scrolling individually.
- Tags have a scope now. Existing tags will get global scope in the database
  migration.

## New features

- Tags have a scope now. Tags created by a basic user are only visible by that
  user. Tags created by an admin/support role can be configured to be visible by
  all users (global scope) or only be admin/support role.
- Re-sampling support for running (requires a recent `cc-metric-store`) and
  archived jobs. This greatly speeds up loading of large or very long jobs. You
  need to add the new configuration key `enable-resampling` to the `config.json`
  file.
- For finished jobs a total job energy is shown in the job view.
- Continuous scrolling in job lists is default now.
- All database queries (especially for sqlite) were optimized resulting in
  dramatically faster load times.
- A performance and energy footprint can be freely configured on a per
  subcluster base. One can filter for footprint statistics for running and
  finished jobs.

## Known issues

- Currently energy footprint metrics of type energy are ignored for calculating
  total energy.
- Resampling for running jobs only works with cc-metric-store
- With energy footprint metrics of type power the unit is ignored and it is
  assumed the metric has the unit Watt.

## Download

[Download the release on GitHub!](https://github.com/ClusterCockpit/cc-backend/releases/tag/v1.4.0)
