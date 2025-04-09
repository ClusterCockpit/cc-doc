---
title: Configuration
description: >
  ClusterCockpit Metric Store Configuration Option References
categories: [cc-metric-store]
tags: [Backend]
weight: 2
---

Configuration options are located in a JSON file. Default path is `config.json`
in current working directory. Alternative paths to the configuration file can be
specified using the command line switch `-config <filename>`.

All durations are specified as string that will be parsed [like
this](https://pkg.go.dev/time#ParseDuration) (Allowed suffixes: `s`, `m`, `h`,
...).

Recognized attributes:

- `metrics`: Map of metric-name to objects with the following properties
(required)
  - `frequency`: Timestep/Interval/Resolution of this metric (required)
  - `aggregation`: Can be `"sum"`, `"avg"` or `null` (required)
    - `null` means aggregation across nodes is forbidden for this metric
    - `"sum"` means that values from the child levels are summed up for the
    parent level
    - `"avg"` means that values from the child levels are averaged for the
    parent level
- `nats`: (optionals)
  - `address`: Url of NATS.io server, example: "nats://localhost:4222"
  - `username` and `password`: Optional, if provided use those for the connection
  - `subscriptions`:
    - `subscribe-to`: Where to expect the measurements to be published
    - `cluster-tag`: Default value for the cluster tag
- `http-api`: (required)
  - `address`: Address to bind to, for example `0.0.0.0:8080` (required)
  - `https-cert-file` and `https-key-file`:  if provided enable HTTPS
  using those files as certificate/key (optional)
- `jwt-public-key`: Base64 encoded string, use this to verify requests to the
HTTP API (required)
- `retention-on-memory`: Keep all values in memory for at least that amount of
time (required)
- `checkpoints`: (required)
  - `interval`: Do checkpoints every X seconds/minutes/hours (required)
  - `directory`: Path to a directory (required)
  - `restore`: After a restart, load the last X seconds/minutes/hours of data
  back into memory (required)
- `archive`:
  - `interval`: Move and compress all checkpoints not needed anymore every X
  seconds/minutes/hours (required)
  - `directory`: Path to a directory (required)
