---
title: Release cc-backend v1.3.0
date: 2024-04-15
description: Minor Release
---
## Changelog

### New Features

- feat: Add OpenID Connect Authentication support
- feat: Add cluster config endpoint to rest api
- feat: Add jobs endpoint to retrieve job meta and all job metric data
- feat: Add rest endpoint to add/edit Metadata entry
- feat: Allow to revert db to previous version
- feat: add footprint card displaying basic metrics
- feat: add selectable histograms to status view
- feat: prototype infinite scroll implementation

### Security updates

- sec: update dependencies

### Bug fixes

- fix: Adapt tag db queries to also work with mysql/mariadb
- fix: Use peak threshold for render limit maxy
- fix: add acc scope to job query if acc >= 1
- fix: fix scope autoselect on jobview statstable
- fix: make hasnextpage optional parameter, use only if inf scroll configured
- fix: move scroll event behind condition
- fix: multiple accs with identical label, cloned data for single acc
- fix: retrigger gql api at manual refresh
- fix: trigger continuous load condition earlier

Supports job archive version 1 and database version 7.

## Release notes

This is a minor release of `cc-backend`, the API backend and frontend
implementation of ClusterCockpit.

### Breaking changes

This release fixes bugs in the MySQL/MariaDB database schema. For this reason
you have to migrate your database using the `-migrate-db` switch.

## Download

[Download the release on GitHub!](https://github.com/ClusterCockpit/cc-backend/releases/tag/v1.3.0)
