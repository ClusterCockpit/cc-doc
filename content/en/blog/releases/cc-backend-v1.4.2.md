---
title: Release cc-backend v1.4.2
date: 2024-12-11T00:00:00.000Z
description: Bugfix Release
---

## Changelog

### Bug fixes

- fix: add missing sorting parameter to REST API call and test
- fix: footprint peak is default if footprint stat is avg

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

[Download the release on GitHub!](https://github.com/ClusterCockpit/cc-backend/releases/tag/v1.4.2)
